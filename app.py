import dash
import dash_html_components as html
import io
import json
import pandas as pd

from dash.dependencies import Input, Output, State
from flask import request, send_file

from components.change_calculator import parse_data, compute_change, get_summary_statistics, get_scatter_plot, \
    change_download_button
from components.trip import remove_last_point_on_table, add_new_point_on_table, get_style_table, get_map_from_table, \
    optimiser_pipeline
from tab_layout import main_layout, about_me_tab, trip_tab, change_calculator_tab, keyboard_tab

app = dash.Dash(__name__)
app.title = 'wow'
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server
app.layout = main_layout()


@app.callback([Output('table-trip-landmark', 'data'),
               Output('table-trip-landmark', 'style_table'),
               Output('input-trip-landmark', 'value')],
              [Input('map-trip', 'click_lat_lng'),
               Input('button-trip-remove', 'n_clicks'),
               Input('button-trip-reset', 'n_clicks')],
              [State('input-trip-landmark', 'value'),
               State('table-trip-landmark', 'data')])
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
def update_trip_map(data, children):
    children = get_map_from_table(data, children)
    return children


@app.callback(Output('trip-results', 'children'),
              [Input('button-trip-ok', 'n_clicks'),
               Input('button-trip-reset', 'n_clicks')],
              [State('table-trip-landmark', 'data')])
def update_trip_results(trigger_ok, trigger_reset, data):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'button-trip-ok':
        answer = optimiser_pipeline(data)
        return answer
    elif ctx == 'button-trip-reset':
        return ''


@app.callback([Output('dropdown-change-x', 'options'),
               Output('dropdown-change-y', 'options'),
               Output('intermediate-change-result', 'children')],
              [Input('upload-change', 'contents')],
              [State('upload-change', 'filename')])
def update_change_upload(contents, filename):
    if dash.callback_context.triggered:
        df = parse_data(contents, filename)
        if type(df) == pd.DataFrame:
            col_options = [{'label': col, 'value': col} for col in df.columns]
            return col_options, col_options, json.dumps(df.to_json(orient='split', date_format='iso'))
    return [], [], []


@app.callback([Output('change-results', 'children'),
               Output('graph-change-results', 'figure')],
              [Input('button-change-ok', 'n_clicks')],
              [State('intermediate-change-result', 'children'),
               State('dropdown-change-x', 'value'),
               State('input-change-x', 'value'),
               State('dropdown-change-y', 'value'),
               State('input-change-y', 'value')])
def update_change_upload(trigger, df_ser, x_col, x_max, y_col, y_max):
    if trigger:
        try:
            df = pd.read_json(json.loads(df_ser), orient='split')
        except TypeError:
            return ['Please upload a file'], {}
        if x_col is None or y_col is None:
            return ['Please specify columns as axis'], {}
        df = compute_change(df, x_col, x_max, y_col, y_max)
        result_table = get_summary_statistics(df, x_col, y_col)
        fig = get_scatter_plot(df, x_col, y_col)
        return [result_table, change_download_button(df)], fig
    return [], {}


@app.callback(Output('placeholder', 'children'),
              [Input('button_music', 'n_clicks')])
def update_keyboard(trigger):
    if trigger:
        import base64
        sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
        # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
        encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
        return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)


@app.server.route('/download_change_df/', methods=['POST'])
def download_change_result():
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


@app.callback(Output('tab-content', 'children'),
              [Input('tabs-parent', 'value')])
def update_output(tab):
    if tab == 'tab-1':
        return about_me_tab()
    elif tab == 'tab-2':
        return trip_tab()
    elif tab == 'tab-3':
        return change_calculator_tab()
    elif tab == 'tab-3':
        return keyboard_tab()


if __name__ == '__main__':
    app.run_server(debug=True)
