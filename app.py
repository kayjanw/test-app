import dash
import dash_core_components as dcc
import dash_html_components as html
import io
import pandas as pd

from dash.dependencies import Input, Output, State
from flask import request, send_file

from components.change_calculator import compute_change, get_summary_statistics, get_scatter_plot, compute_changes, \
    transpose_dataframe, get_line_plot
from components.helper import violin_plot, print_callback, update_when_upload, change_download_button
from components.trip import remove_last_point_on_table, add_new_point_on_table, get_style_table, get_map_from_table, \
    optimiser_pipeline
from tab_layout import main_layout, about_me_tab, trip_tab, change_calculator_tab, change_over_time_tab, keyboard_tab

app = dash.Dash(__name__)
app.title = 'wow'
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server
app.layout = main_layout()

# Variable
print_function = False


@app.callback([Output('table-trip-landmark', 'data'),
               Output('table-trip-landmark', 'style_table'),
               Output('input-trip-landmark', 'value')],
              [Input('map-trip', 'click_lat_lng'),
               Input('button-trip-remove', 'n_clicks'),
               Input('button-trip-reset', 'n_clicks')],
              [State('input-trip-landmark', 'value'),
               State('table-trip-landmark', 'data')])
@print_callback(print_function)
def update_trip_table(e, trigger_remove, trigger_reset, landmark, data):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'button-trip-remove':
        data = remove_last_point_on_table(data)
    elif ctx == 'button-trip-reset':
        data = []
    else:
        if e is not None:
            lat, lon = e
            data = add_new_point_on_table(lat, lon, landmark, data)
    style_table = get_style_table(data)
    return data, style_table, ''


@app.callback(Output('map-trip', 'children'),
              [Input('table-trip-landmark', 'data')],
              [State('map-trip', 'children')])
@print_callback(print_function)
def update_trip_map(data, children):
    children = get_map_from_table(data, children)
    return children


@app.callback(Output('trip-results', 'children'),
              [Input('button-trip-ok', 'n_clicks'),
               Input('button-trip-reset', 'n_clicks')],
              [State('table-trip-landmark', 'data')])
@print_callback(print_function)
def update_trip_results(trigger_ok, trigger_reset, data):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'button-trip-ok':
        return optimiser_pipeline(data)
    elif ctx == 'button-trip-reset':
        return ''


@app.callback([Output('dropdown-change-worksheet', 'options'),
               Output('change-select-worksheet', 'style'),
               Output('change-sample-data', 'children'),
               Output('intermediate-change-result', 'data')],
              [Input('upload-change', 'contents'),
               Input('dropdown-change-worksheet', 'value')],
              [State('upload-change', 'filename'),
               State('change-select-worksheet', 'style')])
@print_callback(print_function)
def update_change_upload(contents, worksheet, filename, style):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    return update_when_upload(contents, worksheet, filename, style, ctx)


@app.callback([Output('dropdown-change-x', 'options'),
               Output('dropdown-change-y', 'options')],
              [Input('intermediate-change-result', 'data')])
@print_callback(print_function)
def update_change_dropdown_options(records):
    if 'df' in records:
        df = pd.read_json(records['df'], orient='split')
        col_options = [{'label': col, 'value': col} for col in df.columns]
        return col_options, col_options
    return [], []


@app.callback([Output('dropdown-change-x', 'value'),
               Output('dropdown-change-y', 'value')],
              [Input('dropdown-change-x', 'options'),
               Input('dropdown-change-y', 'options')],
              [State('dropdown-change-x', 'value'),
               State('dropdown-change-y', 'value')])
@print_callback(print_function)
def update_change_dropdown_value(x_options, y_options, x_value, y_value):
    x_options_list = [opt['label'] for opt in x_options]
    y_options_list = [opt['label'] for opt in y_options]
    if x_value not in x_options_list:
        x_value = None
    if y_value not in y_options_list:
        y_value = None
    return x_value, y_value


@app.callback([Output('change-result', 'children'),
               Output('graph-change-result', 'figure')],
              [Input('button-change-ok', 'n_clicks')],
              [State('intermediate-change-result', 'data'),
               State('dropdown-change-x', 'value'),
               State('input-change-x', 'value'),
               State('dropdown-change-y', 'value'),
               State('input-change-y', 'value')])
@print_callback(print_function)
def update_change_result(trigger, records, x_col, x_max, y_col, y_max):
    if trigger:
        if 'df' in records:
            df = pd.read_json(records['df'], orient='split')
        else:
            return ['Please upload a file'], {}
        if x_col is None or y_col is None:
            return ['Please specify columns as axis'], {}
        if x_col == y_col:
            return ['Please select different columns for comparison'], {}
        df = compute_change(df, x_col, x_max, y_col, y_max)
        result_table = get_summary_statistics(df, x_col, y_col)
        fig = get_scatter_plot(df, x_col, y_col)
        return [result_table, change_download_button(df)], fig
    return [], {}


@app.callback([Output('dropdown-changes-worksheet', 'options'),
               Output('changes-select-worksheet', 'style'),
               Output('changes-sample-data', 'children'),
               Output('intermediate-changes-result', 'data')],
              [Input('upload-changes', 'contents'),
               Input('dropdown-changes-worksheet', 'value')],
              [State('upload-changes', 'filename'),
               State('changes-select-worksheet', 'style')])
@print_callback(print_function)
def update_changes_upload(contents, worksheet, filename, style):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    return update_when_upload(contents, worksheet, filename, style, ctx)


@app.callback([Output('table-changes', 'dropdown'),
               Output('dropdown-changes-identifier', 'options')],
              [Input('intermediate-changes-result', 'data')])
@print_callback(print_function)
def update_changes_dropdown_options(records):
    if 'df' in records:
        df = pd.read_json(records['df'], orient='split')
        col_options = [{'label': col, 'value': col} for col in df.columns]
        return dict(column=dict(options=col_options)), col_options
    return {}, []


@app.callback(Output('table-changes', 'data'),
              [Input('button-changes-add', 'n_clicks')],
              [State('table-changes', 'data')])
@print_callback(print_function)
def update_changes_add_row(trigger, data):
    if trigger:
        data.append(dict(column='', max=''))
    return data


@app.callback([Output('changes-result', 'children'),
               Output('div-changes-result', 'children')],
              [Input('button-changes-ok', 'n_clicks')],
              [State('intermediate-changes-result', 'data'),
               State('dropdown-changes-identifier', 'value'),
               State('table-changes', 'data')])
@print_callback(print_function)
def update_changes_result(trigger, records, col_identifier, data):
    instructions = []
    graph = []
    if trigger:
        list_of_tuples = [(row['column'], row['max']) for row in data
                          if row['column'] is not ''
                          if row['column'] is not None]
        if 'df' in records and len(list_of_tuples):
            df = pd.read_json(records['df'], orient='split')
            df = compute_changes(df, list_of_tuples)
            if len(df):
                df2 = transpose_dataframe(df, col_identifier, list_of_tuples)
                instructions, fig = get_line_plot(df2)
                graph = [html.P(f'Number of processed rows: {len(df)}'),
                         dcc.Graph(figure=fig, id='graph-changes-result')]
            elif not len(df):
                instructions = ['Processed dataframe is empty. Please select numeric columns']
        elif 'df' not in records:
            instructions = ['Please upload a file']
        elif not len(list_of_tuples):
            instructions = ['Please specify columns to compare']
    return instructions, graph


@app.callback(Output('graph-changes-result', 'figure'),
              [Input('graph-changes-result', 'hoverData')],
              [State('graph-changes-result', 'figure')])
def update_changes_hover(hover_data, figure):
    for trace in figure['data']:
        trace["line"]["width"] = 1
        trace["opacity"] = 0.7
    if hover_data:
        trace_index = hover_data['points'][0]['curveNumber']
        figure['data'][trace_index]['line']['width'] = 3
        figure['data'][trace_index]['opacity'] = 1
    return figure


@app.callback(Output('placeholder', 'children'),
              [Input('button_music', 'n_clicks')])
@print_callback(print_function)
def update_keyboard(trigger):
    if trigger:
        import base64
        sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
        # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
        encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
        return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)


@app.callback(Output('tab-content', 'children'),
              [Input('tabs-parent', 'value')])
@print_callback(print_function)
def update_output(tab):
    if tab == 'tab-1':
        return about_me_tab()
    elif tab == 'tab-2':
        return trip_tab()
    elif tab == 'tab-3':
        return change_calculator_tab()
    elif tab == 'tab-4':
        return change_over_time_tab()
    elif tab == 'tab-5':
        return keyboard_tab()
    else:
        return dcc.Graph(
            figure=violin_plot(),
            config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                           'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'hoverClosestCartesian',
                                           'hoverCompareCartesian'],
            },
            style={
                'margin-top': '15vh',
                'height': '60vh'
            }
        )


@app.server.route('/download_df/', methods=['POST'])
def download_result():
    df = request.form.get('result')
    df = pd.read_json(df, orient='split')
    if len(df)>0:
        buf = io.BytesIO()
        excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
        df.to_excel(excel_writer, sheet_name="Sheet1")
        excel_writer.save()
        excel_data = buf.getvalue()
        buf.seek(0)
        return send_file(
            buf,
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            attachment_filename="result.xlsx",
            as_attachment=True,
            cache_timeout=0
        )


if __name__ == '__main__':
    app.run_server(debug=True)
