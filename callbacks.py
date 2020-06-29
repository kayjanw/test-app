import dash
import dash_core_components as dcc
import traceback
from dash.dependencies import Input, Output, State

from components.change_calculator import ChangeCalculator
from components.helper import violin_plot, print_callback, get_summary_statistics, decode_df, update_when_upload, \
    result_download_button
from components.mbti import MBTI
from components.trip_planner import TripPlanner
from layouts import app_1, app_2, about_me_tab, trip_tab, change_tab, changes_tab, mbti_tab


def register_callbacks(app, print_function):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    @print_callback(print_function)
    def display_page(pathname):
        """Display page based on URL

        Args:
            pathname (str): url path

        Returns:
            (html.Div)
        """
        if pathname == '/':
            return app_1()
        else:
            return app_2(pathname)

    @app.callback([Output('sidebar-big', 'style'),
                   Output('sidebar-small', 'style'),
                   Output('tab-content', 'style')],
                  [Input('button-sidebar', 'n_clicks'),
                   Input('tabs-parent', 'value')],
                  [State('sidebar-big', 'style'),
                   State('sidebar-small', 'style'),
                   State('tab-content', 'style')])
    @print_callback(print_function)
    def display_sidebar_mobile(trigger_sidebar, trigger_tab, style_sidebar_left, style_sidebar_top, style_contents):
        """Display sidebar on icon click (mobile device)

        Args:
            trigger_sidebar: trigger on button click on sidebar
            trigger_tab: trigger on tab change
            style_sidebar_left: current style of left sidebar
            style_sidebar_top: current style of top sidebar
            style_contents: current style of tab content

        Returns:
        3-element tuple

        - (dict): updated style of left sidebar
        - (dict): updated style of top sidebar
        - (dict): updated style of tab content
        """
        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if ctx == 'button-sidebar':
            if isinstance(style_sidebar_left, dict) and style_sidebar_left['display'] == 'inline-block':
                # Collapse left sidebar
                style_sidebar_left['display'] = 'none'
                style_sidebar_top['margin-left'] = '0'
                style_contents['margin-left'] = '0'
                style_contents['position'] = 'absolute'
            else:
                # Show left sidebar
                style_sidebar_left = {'display': 'inline-block'}
                style_sidebar_top = {'margin-left': '85vw'}
                style_contents = {'margin-left': '85vw', 'position': 'fixed'}
        elif ctx == 'tabs-parent':
            # Collapse left sidebar
            style_sidebar_left['display'] = 'none'
            style_sidebar_top['margin-left'] = '0'
            style_contents['margin-left'] = '0'
            style_contents['position'] = 'absolute'
        return style_sidebar_left, style_sidebar_top, style_contents

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
        """Update trip table

        Args:
            e (tuple): trigger on map click
            trigger_remove: trigger on button click
            trigger_reset: trigger on button click
            landmark (str): name of landmark to be added
            data (list): data of table that displays landmarks information

        Returns:
            3-element tuple

            - (list): updated data of table that displays landmarks information
            - (dict): style of table that displays landmarks information
            - (str): reset name of next landmark to be added
        """
        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if ctx == 'button-trip-remove':
            data = TripPlanner().remove_last_point_on_table(data)
        elif ctx == 'button-trip-reset':
            data = []
        else:
            if e is not None:
                lat, lon = e
                data = TripPlanner().add_new_point_on_table(lat, lon, landmark, data)
        style_table = TripPlanner().get_style_table(data)
        return data, style_table, ''

    @app.callback(Output('map-trip', 'children'),
                  [Input('table-trip-landmark', 'data')],
                  [State('map-trip', 'children')])
    @print_callback(print_function)
    def update_trip_map(data, children):
        """Update trip map to include landmark location pin

        Args:
            data (list): data of table that displays landmarks information, triggers callback
            children (list): current map children

        Returns:
            (list): updated map children
        """
        children = TripPlanner().get_map_from_table(data, children)
        return children

    @app.callback(Output('trip-results', 'children'),
                  [Input('button-trip-ok', 'n_clicks'),
                   Input('button-trip-reset', 'n_clicks')],
                  [State('table-trip-landmark', 'data')])
    @print_callback(print_function)
    def update_trip_results(trigger_ok, trigger_reset, data):
        """Update and display trip results

        Args:
            trigger_ok: trigger on button click
            trigger_reset: trigger on button click
            data (list): data of table that displays landmarks information

        Returns:
            (str/list)
        """
        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if ctx == 'button-trip-ok':
            return TripPlanner().optimiser_pipeline(data)
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
        """Update change calculator interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            worksheet (str): worksheet of excel file, if applicable, triggers callback
            filename (str): filename of data uploaded
            style (dict): current style of worksheet selector dropdown

        Returns:
            4-element tuple

            - (list): list of worksheets options
            - (dict): updated style of worksheet selector dropdown
            - (dash_table.DataTable/list): sample of uploaded data
            - (dict): intermediate data stored in dcc.Store
        """
        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        return update_when_upload(contents, worksheet, filename, style, ctx)

    @app.callback([Output('dropdown-change-x', 'options'),
                   Output('dropdown-change-y', 'options')],
                  [Input('intermediate-change-result', 'data')])
    @print_callback(print_function)
    def update_change_dropdown_options(records):
        """Update change calculator column selector dropdown options

        Args:
            records (dict): intermediate data stored in dcc.Store

        Returns:
            2-element tuple

            - (list): column selector dropdown options for x-axis
            - (list): column selector dropdown options for y-axis
        """
        if 'df' in records:
            df = decode_df(records['df'])
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
        """Update change calculator column selector dropdown value

        Args:
            x_options (list): column selector dropdown options for x-axis, triggers callback
            y_options (list): column selector dropdown options for y-axis, triggers callback
            x_value (str): current column selector dropdown value for x-axis
            y_value (str): current column selector dropdown value for y-axis

        Returns:
            2-element tuple

            - (str): updated column selector dropdown value for x-axis
            - (str): updated column selector dropdown value for y-axis
        """
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
        """Update and display change calculator results

        Args:
            trigger: trigger on button click
            records (dict): intermediate data stored in dcc.Store
            x_col (str): column for x-axis, could be None
            x_max (int): maximum value for x-axis, could be None or empty string
            y_col (str): column for x-axis, could be None
            y_max (int): maximum value for y-axis, could be None or empty string

        Returns:
            2-element tuple

            - (list): div result of change calculator
            - (dict): graphical result of change calculator
        """
        result = []
        fig = {}
        if trigger:
            if 'df' in records and x_col is not None and y_col is not None and x_col != y_col:
                df = decode_df(records['df'])
                df = ChangeCalculator().compute_change(df, x_col, x_max, y_col, y_max)
                result_table = get_summary_statistics(df, [x_col, y_col])
                result = [result_table, result_download_button(df)]
                fig = ChangeCalculator().get_scatter_plot(df, x_col, y_col)
            elif 'df' not in records:
                result = ['Please upload a file']
            elif x_col is None or y_col is None:
                result = ['Please specify columns as axis']
            elif x_col == y_col:
                result = ['Please select different columns for comparison']
        return result, fig

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
        """Update change calculator 2 interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            worksheet (str): worksheet of excel file, if applicable, triggers callback
            filename (str): filename of data uploaded
            style (dict): current style of worksheet selector dropdown

        Returns:
            4-element tuple

            - (list): list of worksheets options
            - (dict): updated style of worksheet selector dropdown
            - (dash_table.DataTable/list): sample of uploaded data
            - (dict): intermediate data stored in dcc.Store
        """
        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        return update_when_upload(contents, worksheet, filename, style, ctx)

    @app.callback([Output('table-changes', 'dropdown'),
                   Output('dropdown-changes-identifier', 'options')],
                  [Input('intermediate-changes-result', 'data')])
    @print_callback(print_function)
    def update_changes_dropdown_options(records):
        """Update change calculator 2 column selector dropdown options

        Args:
            records (dict): intermediate data stored in dcc.Store

        Returns:
            2-element tuple

            - (list): column selector dropdown options for table
            - (list): column selector dropdown options for column indicators
        """
        if 'df' in records:
            df = decode_df(records['df'])
            col_options = [{'label': col, 'value': col} for col in df.columns]
            return dict(column=dict(options=col_options)), col_options
        return {}, []

    @app.callback(Output('table-changes', 'data'),
                  [Input('button-changes-add', 'n_clicks')],
                  [State('table-changes', 'data')])
    @print_callback(print_function)
    def update_changes_add_row(trigger, data):
        """Update and adds additional row to change calculator 2 table

        Args:
            trigger: trigger on button click
            data (list): data of table that stores comparison column information

        Returns:
            (list): updated data of table that stores comparison column information
        """
        if trigger:
            data.append(dict(column='', max=''))
        return data

    @app.callback([Output('changes-result', 'children'),
                   Output('changes-result', 'style'),
                   Output('div-changes-result', 'children')],
                  [Input('button-changes-ok', 'n_clicks')],
                  [State('intermediate-changes-result', 'data'),
                   State('dropdown-changes-identifier', 'value'),
                   State('table-changes', 'data')])
    @print_callback(print_function)
    def update_changes_result(trigger, records, col_identifier, data):
        """Update and display change calculator 2 results

        Args:
            trigger: trigger on button click
            records (dict): intermediate data stored in dcc.Store
            col_identifier (str): column for index, could be None
            data (list): data of table that stores comparison column information

        Returns:
            3-element tuple

            - (list): div result of change calculator 2
            - (dict): style of div result of change calculator 2
            - (dict): graphical result of change calculator 2
        """
        summary = []
        style = {'display': 'none'}
        graph = []
        if trigger:
            style = {'display': 'block'}
            list_of_tuples = [(row['column'], row['max']) for row in data
                              if row['column'] is not ''
                              if row['column'] is not None]
            cols = list(dict.fromkeys([row[0] for row in list_of_tuples]))
            if 'df' in records and len(list_of_tuples):
                df = decode_df(records['df'])
                df = ChangeCalculator().compute_changes(df, col_identifier, list_of_tuples)
                if len(df):
                    df2 = ChangeCalculator().transpose_dataframe(df, col_identifier, cols)
                    result_table = get_summary_statistics(df, cols)
                    instructions_box, fig_box = ChangeCalculator().get_box_plot(df, cols)
                    instructions_line, fig_line = ChangeCalculator().get_line_plot(df2)
                    summary = ['Summary statistics:', result_table] + instructions_box + [dcc.Graph(figure=fig_box)]
                    graph = instructions_line + [dcc.Graph(figure=fig_line, id='graph-changes-result')]
                elif not len(df):
                    summary = ['Processed dataframe is empty. Please select numeric columns']
            elif 'df' not in records:
                summary = ['Please upload a file']
            elif not len(list_of_tuples):
                summary = ['Please specify columns to compare']
        return summary, style, graph

    @app.callback(Output('graph-changes-result', 'figure'),
                  [Input('graph-changes-result', 'hoverData')],
                  [State('graph-changes-result', 'figure')])
    def update_changes_hover(hover_data, figure):
        """Update layout of plotly graph on hover

        Args:
            hover_data: trigger on hover
            figure (dict): figure for plot

        Returns:
            (dict): updated figure for plot
        """
        for trace in figure['data']:
            trace["line"]["width"] = 1
            trace["opacity"] = 0.7
        if hover_data:
            trace_index = hover_data['points'][0]['curveNumber']
            figure['data'][trace_index]['line']['width'] = 3
            figure['data'][trace_index]['opacity'] = 1
        return figure

    @app.callback(Output('text-mbti-words', 'children'),
                  [Input('input-mbti', 'value')])
    def update_mbti_words(input_text):
        """Update number of input words in vocabulary

        Args:
            input_text (str): input text

        Returns:
            (str)
        """
        try:
            n_words = MBTI().get_num_words(input_text)
            return f'{n_words} word(s) in vocabulary'
        except Exception as e:
            return f'Error loading number of word(s). Error message: {e}'

    @app.callback([Output('graph-mbti', 'figure'),
                   Output('graph-mbti', 'style')],
                  [Input('button-mbti', 'n_clicks')],
                  [State('input-mbti', 'value'),
                   State('graph-mbti', 'style')])
    def update_mbti_result(trigger, input_text, style):
        """Update results of mbti personality results and graph

        Args:
            trigger: Trigger on button click
            input_text (str): input text
            style (dict): style of graphical result of mbti model

        Returns:
            3-element tuple

            - (list): div result of mbti model
            - (dict): graphical result of mbti model
            - (dict): updated style of graphical result of mbti model
        """
        plot = {}
        style['display'] = 'none'
        if trigger:
            try:
                personality, predictions = MBTI().test_pipeline(input_text)
                plot = MBTI().get_bar_plot(predictions, personality)
                style['display'] = 'block'
                style['height'] = 400
            except Exception as e:
                print(traceback.print_exc())
        return plot, style

    # @app.callback(Output('placeholder', 'children'),
    #               [Input('button_music', 'n_clicks')])
    # @print_callback(print_function)
    # def update_keyboard(trigger):
    #     if trigger:
    #         import base64
    #         sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
    #         # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
    #         encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
    #         return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)

    @app.callback(Output('tab-content', 'children'),
                  [Input('tabs-parent', 'value')])
    @print_callback(print_function)
    def update_output(tab):
        """Update content when tab changes

        Args:
            tab: trigger on tab change

        Returns:
            (html.Div)
        """
        if tab == 'tab-1':
            return about_me_tab()
        elif tab == 'tab-2':
            return trip_tab()
        elif tab == 'tab-3':
            return change_tab()
        elif tab == 'tab-4':
            return changes_tab()
        elif tab == 'tab-5':
            return mbti_tab()
        else:
            return dcc.Graph(
                figure=violin_plot(),
                id='violin-plot',
                config={
                    'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                               'autoScale2d', 'resetScale2d', 'toggleSpikelines',
                                               'hoverClosestCartesian', 'hoverCompareCartesian'],
                },
                style={
                    'margin-top': '15vh',
                    'height': '60vh'
                }
            )
