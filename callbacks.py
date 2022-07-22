import dash
import json
import traceback

from dash import dcc, html
from dash.dependencies import Input, Output, State

from components import (
    ChangeCalculator,
    ChatAnalyzer,
    EventPlanner,
    MBTI,
    RandomGenerator,
    TradeSocket,
    TripPlanner,
    WNRS,
)
from components.helper import (
    return_message,
    print_callback,
    violin_plot,
    dcc_loading,
    parse_data,
    generate_datatable,
    get_summary_statistics,
    encode_df,
    decode_df,
    encode_dict,
    decode_dict,
    update_when_upload,
    result_download_button,
    valid_email,
    send_email,
)
from layouts import (
    app_1,
    app_2,
    app_event,
    about_me_tab,
    change_tab,
    changes_tab,
    chat_tab,
    trip_tab,
    mbti_tab,
    trade_tab,
    event_tab,
    rng_tab,
    wnrs_tab,
    contact_tab,
    image_edit_tab,
)


def register_callbacks(app, print_function):
    inline_style = {"display": "inline-block"}
    flex_style = {"display": "flex"}
    hide_style = {"display": "none"}
    show_button_style = {"background-color": "#BE9B89"}
    hide_button_style = {"background-color": "#F0E3DF"}

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    @print_callback(print_function)
    def display_page(pathname):
        """Display page based on URL

        Args:
            pathname (str): url path

        Returns:
            html.Div
        """
        if pathname == "/":
            return app_1()
        elif pathname == "/event":
            return app_event()
        else:
            return app_2(pathname)

    @app.callback([Output("sidebar", "style"),
                   Output("banner", "style"),
                   Output("tab-content", "style")],
                  [Input("button-sidebar", "n_clicks"),
                   Input("tabs-parent", "value")],
                  [State("sidebar", "style"),
                   State("banner", "style"),
                   State("tab-content", "style")])
    @print_callback(print_function)
    def display_sidebar_mobile(trigger_sidebar, trigger_tab, style_sidebar, style_banner, style_contents):
        """Display sidebar on icon click (mobile device)

        Args:
            trigger_sidebar: trigger on button click on sidebar
            trigger_tab: trigger on tab change
            style_sidebar: current style of sidebar
            style_banner: current style of banner
            style_contents: current style of tab content

        Returns:
        3-element tuple

        - dict: updated style of sidebar
        - dict: updated style of banner
        - dict: updated style of tab content
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        if ctx == "button-sidebar":
            if isinstance(style_sidebar, dict) and style_sidebar["display"] == "inline-block":
                # Collapse left sidebar
                style_sidebar["display"] = "none"
                style_banner["margin-left"] = "0"
                style_contents["margin-left"] = "0"
                style_contents["position"] = "absolute"
            else:
                # First assignment, show left sidebar
                style_sidebar = {"display": "inline-block"}
                style_banner = {"margin-left": "85vw"}
                style_contents = {"margin-left": "85vw", "position": "fixed"}
        elif ctx == "tabs-parent":
            if isinstance(style_sidebar, dict):
                # Collapse left sidebar
                style_sidebar = {"display": "none"}
                style_banner = {"margin-left": "0"}
                style_contents = {"margin-left": "0", "position": "absolute"}
        return style_sidebar, style_banner, style_contents

    @app.callback([Output("dropdown-change-worksheet", "options"),
                   Output("change-select-worksheet", "style"),
                   Output("change-sample-data", "children"),
                   Output("intermediate-change-result", "data")],
                  [Input("upload-change", "contents"),
                   Input("dropdown-change-worksheet", "value")],
                  [State("upload-change", "filename"),
                   State("change-select-worksheet", "style")])
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

            - list: list of worksheets options
            - dict: updated style of worksheet selector dropdown
            - dash_table.DataTable/list: sample of uploaded data
            - dict: intermediate data stored in dcc.Store
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        return update_when_upload(contents, worksheet, filename, style, ctx)

    @app.callback([Output("dropdown-change-x", "options"),
                   Output("dropdown-change-y", "options")],
                  [Input("intermediate-change-result", "data")])
    @print_callback(print_function)
    def update_change_dropdown_options(records):
        """Update change calculator column selector dropdown options

        Args:
            records (dict): intermediate data stored in dcc.Store

        Returns:
            2-element tuple

            - list: column selector dropdown options for x-axis
            - list: column selector dropdown options for y-axis
        """
        if "df" in records:
            df = decode_df(records["df"])
            col_options = [{"label": col, "value": col} for col in df.columns]
            return col_options, col_options
        return [], []

    @app.callback([Output("dropdown-change-x", "value"),
                   Output("dropdown-change-y", "value")],
                  [Input("dropdown-change-x", "options"),
                   Input("dropdown-change-y", "options")],
                  [State("dropdown-change-x", "value"),
                   State("dropdown-change-y", "value")],)
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

            - str: updated column selector dropdown value for x-axis
            - str: updated column selector dropdown value for y-axis
        """
        x_options_list = [opt["label"] for opt in x_options]
        y_options_list = [opt["label"] for opt in y_options]
        if x_value not in x_options_list:
            x_value = None
        if y_value not in y_options_list:
            y_value = None
        return x_value, y_value

    @app.callback([Output("change-result-error", "children"),
                   Output("div-change-result", "style"),
                   Output("change-result", "children"),
                   Output("graph-change-result", "figure")],
                  [Input("button-change-ok", "n_clicks")],
                  [State("intermediate-change-result", "data"),
                   State("dropdown-change-x", "value"),
                   State("input-change-x", "value"),
                   State("dropdown-change-y", "value"),
                   State("input-change-y", "value")])
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
            4-element tuple

            - list: div result of change calculator error (if any)
            - dict: updated style of change calculator div
            - list: div result of change calculator
            - dict: graphical result of change calculator
        """
        result_error = []
        style = hide_style
        result = []
        fig = {}
        if trigger:
            if "df" in records and x_col is not None and y_col is not None and x_col != y_col:
                result_error = [return_message["scroll_down"]]
                style = inline_style
                df = decode_df(records["df"])
                df = ChangeCalculator().compute_change(df, x_col, x_max, y_col, y_max)
                result_table = get_summary_statistics(df, [x_col, y_col], dark=False)
                result = [
                    html.H5("Summary Statistics"),
                    result_table,
                    result_download_button(app, df)
                ]
                fig = ChangeCalculator().get_scatter_plot(df, x_col, y_col)
            elif "df" not in records:
                result_error = [return_message["file_not_uploaded"]]
            elif x_col is None or y_col is None:
                result_error = [return_message["change_axis"]]
            elif x_col == y_col:
                result_error = [return_message["change_columns"]]
        return result_error, style, result, fig

    @app.callback([Output("dropdown-changes-worksheet", "options"),
                   Output("changes-select-worksheet", "style"),
                   Output("changes-sample-data", "children"),
                   Output("intermediate-changes-result", "data")],
                  [Input("upload-changes", "contents"),
                   Input("dropdown-changes-worksheet", "value")],
                  [State("upload-changes", "filename"),
                   State("changes-select-worksheet", "style")])
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

            - list: list of worksheets options
            - dict: updated style of worksheet selector dropdown
            - dash_table.DataTable/list: sample of uploaded data
            - dict: intermediate data stored in dcc.Store
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        return update_when_upload(contents, worksheet, filename, style, ctx)

    @app.callback([Output("table-changes", "dropdown"),
                   Output("dropdown-changes-identifier", "options")],
                  [Input("intermediate-changes-result", "data")])
    @print_callback(print_function)
    def update_changes_dropdown_options(records):
        """Update change calculator 2 column selector dropdown options

        Args:
            records (dict): intermediate data stored in dcc.Store

        Returns:
            2-element tuple

            - list: column selector dropdown options for table
            - list: column selector dropdown options for column indicators
        """
        if "df" in records:
            df = decode_df(records["df"])
            col_options = [{"label": col, "value": col} for col in df.columns]
            return dict(column=dict(options=col_options)), col_options
        return {}, []

    @app.callback(Output("table-changes", "data"),
                  [Input("button-changes-add", "n_clicks")],
                  [State("table-changes", "data")])
    @print_callback(print_function)
    def update_changes_add_row(trigger, data):
        """Update and adds additional row to change calculator 2 table

        Args:
            trigger: trigger on button click
            data (list): data of table that stores comparison column information

        Returns:
            list: updated data of table that stores comparison column information
        """
        if trigger:
            data.append(dict(column="", max=""))
        return data

    @app.callback([Output("changes-result-error", "children"),
                   Output("div-changes-result", "style"),
                   Output("changes-result", "children"),
                   Output("graph-changes-boxplot", "figure"),
                   Output("graph-changes-result", "children")],
                  [Input("button-changes-ok", "n_clicks")],
                  [State("intermediate-changes-result", "data"),
                   State("dropdown-changes-identifier", "value"),
                   State("table-changes", "data")])
    @print_callback(print_function)
    def update_changes_result(trigger, records, col_identifier, data):
        """Update and display change calculator 2 results

        Args:
            trigger: trigger on button click
            records (dict): intermediate data stored in dcc.Store
            col_identifier (str): column for index, could be None
            data (list): data of table that stores comparison column information

        Returns:
            4-element tuple

            - list: div result of change calculator 2 error (if any)
            - list: div result of change calculator 2
            - dict: style of div result of change calculator 2
            - dict: graphical result of change calculator 2
        """
        result_error = []
        style = hide_style
        result = []
        fig_box = {}
        graph = []
        if trigger:
            list_of_tuples = [
                (row["column"], row["max"])
                for row in data
                if row["column"]
            ]
            cols = list(dict.fromkeys([row[0] for row in list_of_tuples]))
            if "df" in records and len(list_of_tuples):
                result_error = [return_message["scroll_down"]]
                style = inline_style
                df = decode_df(records["df"])
                df = ChangeCalculator().compute_changes(
                    df, col_identifier, list_of_tuples
                )
                if len(df):
                    df2 = ChangeCalculator().transpose_dataframe(df, col_identifier, cols)
                    result_table = get_summary_statistics(df, cols)
                    fig_box = ChangeCalculator().get_box_plot(df, cols)
                    instructions_line, fig_line = ChangeCalculator().get_line_plot(app, df2)
                    result = [
                        html.H5("Summary Statistics"),
                        result_table
                    ]
                    graph = instructions_line + [dcc.Graph(figure=fig_line, id="graph-changes-line")]
                elif not len(df):
                    result_error = [return_message["change_numeric"]]
            elif "df" not in records:
                result_error = [return_message["file_not_uploaded"]]
            elif not len(list_of_tuples):
                result_error = [return_message["change_columns_empty"]]
        return result_error, style, result, fig_box, graph

    @app.callback(Output("graph-changes-line", "figure"),
                  [Input("graph-changes-line", "hoverData")],
                  [State("graph-changes-line", "figure")])
    @print_callback(print_function)
    def update_changes_hover(hover_data, figure):
        """Update layout of plotly graph on hover

        Args:
            hover_data: trigger on hover
            figure (dict): figure for plot

        Returns:
            dict: updated figure for plot
        """
        for trace in figure["data"]:
            trace["line"]["width"] = 1
            trace["opacity"] = 0.7
        if hover_data:
            trace_index = hover_data["points"][0]["curveNumber"]
            figure["data"][trace_index]["line"]["width"] = 3
            figure["data"][trace_index]["opacity"] = 1
        return figure

    # @app.callback(Output('text-chat-loading', 'children'),
    #               [Input('upload-chat', 'contents')])
    # def update_chat_upload_loading(contents):
    #     content = []
    #     if dash.callback_context.triggered:
    #         content = ['Uploading chat...']
    #     return html.P(content, id='text-chat-confirm')

    @app.callback([Output("text-chat-confirm", "children"),
                   Output("intermediate-chat-result", "data")],
                  [Input("upload-chat", "contents")],
                  [State("upload-chat", "filename")])
    @print_callback(print_function)
    def update_chat_upload(contents, filename):
        """Update chat analyzer interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded

        Returns:
            2-element tuple

            - list: message of upload status
            - str: intermediate data stored in dcc.Store
        """
        upload_message = ""
        storage = {}
        if dash.callback_context.triggered:
            if "json" not in filename:
                upload_message = [return_message["file_not_uploaded_json"]]
            else:
                data = parse_data(contents, filename)
                try:
                    chat = ChatAnalyzer(data=data)
                    upload_message = [f"Chat uploaded: {chat.chat_name}"]
                    storage = contents
                except AssertionError as e:
                    upload_message = [f"Error: {e}"]
                except KeyError:
                    upload_message = [return_message["wrong_format_json"]]
        return upload_message, storage

    @app.callback([Output("chat-result-error", "children"),
                   Output("div-chat-result", "style"),
                   Output("chat-result", "children"),
                   Output("graph-chat-result-day", "figure"),
                   Output("graph-chat-result-hour", "figure"),
                   Output("chat-result-wordcloud", "children")],
                  [Input("button-chat-ok", "n_clicks")],
                  [State("intermediate-chat-result", "data")])
    @print_callback(print_function)
    def update_chat_result(trigger, contents):
        """Update and display chat analyzer results

        Args:
            trigger: trigger on button click
            contents (str): intermediate data stored in dcc.Store

        Returns:
            6-element tuple

            - list: div result of chat analyzer error (if any)
            - dict: updated style of chat analyzer div
            - list: div result of chat analyzer
            - dict: graphical result 1 of chat analyzer
            - dict: graphical result 2 of chat analyzer
            - list: graphical result 3 of chat analyzer
        """
        result_error = []
        style = hide_style
        result = []
        fig1 = {}
        fig2 = {}
        fig3 = []
        if trigger:
            if not contents:
                result_error = [return_message["file_not_uploaded"]]
            else:
                style = inline_style
                data = parse_data(contents, "json")
                chat = ChatAnalyzer(data=data)
                processed_df, text_df = chat.process_chat()
                message_info_table = generate_datatable(processed_df, max_rows=len(processed_df), dark=False)
                result = [
                    html.H5("Chat Breakdown"),
                    message_info_table
                ]
                fig1 = chat.get_time_series_hour_plot(text_df)
                fig2 = chat.get_time_series_day_plot(text_df)
                fig3 = chat.get_word_cloud(text_df)
        return result_error, style, result, fig1, fig2, fig3

    @app.callback([Output("table-trip-landmark", "data"),
                   Output("table-trip-landmark", "style_table"),
                   Output("input-trip-landmark", "value")],
                  [Input("map-trip", "click_lat_lng"),
                   Input("button-trip-remove", "n_clicks"),
                   Input("button-trip-reset", "n_clicks")],
                  [State("input-trip-landmark", "value"),
                   State("table-trip-landmark", "data")])
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

            - list: updated data of table that displays landmarks information
            - dict: style of table that displays landmarks information
            - str: reset name of next landmark to be added
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        if ctx == "button-trip-remove":
            data = TripPlanner().remove_last_point_on_table(data)
        elif ctx == "button-trip-reset":
            data = []
        else:
            if e is not None:
                lat, lon = e
                data = TripPlanner().add_new_point_on_table(lat, lon, landmark, data)
        style_table = TripPlanner().get_style_table(data)
        return data, style_table, ""

    @app.callback(Output("map-trip", "children"),
                  [Input("table-trip-landmark", "data")],
                  [State("map-trip", "children")])
    @print_callback(print_function)
    def update_trip_map(data, children):
        """Update trip map to include landmark location pin

        Args:
            data (list): data of table that displays landmarks information, triggers callback
            children (list): current map children

        Returns:
            list: updated map children
        """
        children = TripPlanner().get_map_from_table(data, children)
        return children

    @app.callback(Output("trip-result", "children"),
                  [Input("button-trip-ok", "n_clicks"),
                   Input("button-trip-reset", "n_clicks")],
                  [State("table-trip-landmark", "data")])
    @print_callback(print_function)
    def update_trip_results(trigger_ok, trigger_reset, data):
        """Update and display trip results

        Args:
            trigger_ok: trigger on button click
            trigger_reset: trigger on button click
            data (list): data of table that displays landmarks information

        Returns:
            str/list
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        result = ""
        if ctx == "button-trip-ok":
            try:
                result = TripPlanner().optimiser_pipeline(data)
            except IndexError:
                result = TripPlanner().optimiser_pipeline(data)
        elif ctx == "button-trip-reset":
            pass
        return result

    @app.callback(Output("text-mbti-words", "children"),
                  [Input("input-mbti", "value")])
    @print_callback(print_function)
    def update_mbti_words(input_text):
        """Update number of input words in vocabulary

        Args:
            input_text (str): input text

        Returns:
            str
        """
        try:
            n_words = MBTI().get_num_words(input_text)
            return f"{n_words} word(s) in vocabulary"
        except Exception as e:
            return f"Error loading number of word(s), error message: {e}"

    @app.callback([Output("graph-mbti", "figure"),
                   Output("graph-mbti", "style"),
                   Output("mbti-results", "children")],
                  [Input("button-mbti-ok", "n_clicks")],
                  [State("input-mbti", "value"),
                   State("graph-mbti", "style")])
    @print_callback(print_function)
    def update_mbti_result(trigger, input_text, style):
        """Update results of mbti personality results and graph

        Args:
            trigger: trigger on button click
            input_text (str): input text
            style (dict): style of graphical result of mbti model

        Returns:
            3-element tuple

            - dict: graphical result of mbti model
            - dict: updated style of graphical result of mbti model
            - list: result of mbti model
        """
        plot = {}
        style["display"] = "none"
        personality_details = []
        if trigger:
            try:
                personality, predictions = MBTI().test_pipeline(input_text)
                plot = MBTI().get_bar_plot(predictions)
                personality_details = MBTI().get_personality_details(personality)
                style["display"] = "block"
                style["height"] = 400
            except Exception as e:
                personality_details = [
                    f"Error loading results, error message: {e}. Please try again."
                ]
                print(traceback.print_exc())
        return plot, style, personality_details

    @app.callback([Output("trade-result", "children"),
                   Output("graph-trade", "figure")],
                  Input("interval-trade", "n_intervals"),
                  [State("dropdown-trade-symbol", "value"),
                   State("dropdown-trade-frequency", "value"),
                   State("input-trade-candle", "value"),
                   State("checkbox-trade-ind", "value"),
                   State("radio-trade-forecast", "value")])
    @print_callback(print_function)
    def update_trade_graph(trigger, symbol, frequency, n_candle, indicators_ind, forecast_methods):
        """Update trade candlestick chart

        Args:
            trigger: triggers callback
            symbol (str): symbol to plot for
            frequency (str): frequency of candlestick
            n_candle (int): number of points on candlestick
            indicators_ind (list): list of indicators to plot
            forecast_methods (list): list of forecasting methods

        Returns:
            dict: graphical result of trade
        """
        error_message = ""
        fig = {}
        if symbol and frequency and n_candle:
            try:
                trade = TradeSocket()
                rates_data = trade.get_rates_data(symbol, frequency, n_candle)
                fig = trade.get_candlestick_chart(symbol, n_candle, rates_data, indicators_ind, forecast_methods)
            except Exception as e:
                error_message = f"Error: {e}"
        return error_message, fig

    @app.callback([Output("text-event-confirm", "children"),
                   Output("intermediate-event-result", "data")],
                  [Input("upload-event", "contents")],
                  [State("upload-event", "filename")])
    @print_callback(print_function)
    def update_event_upload(contents, filename):
        """Update event planner interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded

        Returns:
            2-element tuple

            - list: message of upload status
            - str: intermediate data stored in dcc.Store
        """
        upload_message = ""
        storage = {}
        if dash.callback_context.triggered:
            _, _, _, records = update_when_upload(contents, "", filename, {}, "")
            if "df" in records:
                df = decode_df(records["df"])
                if df.columns[0] == "Event:" and df.iloc[1, 0] == "Name" and df.iloc[1, 1] == "Email (Optional)":
                    event = df.columns[1]
                    df = df.iloc[2:, :].rename(columns=df.iloc[1])
                    storage = dict(df=encode_df(df), event=event)
                    upload_message = [return_message["file_uploaded"]]
                else:
                    upload_message = [return_message["wrong_format_demo"]]
            else:
                upload_message = [return_message["wrong_file_type"]]
        return upload_message, storage

    @app.callback([Output("event-result-error", "children"),
                   Output("div-event-result", "style"),
                   Output("div-event-result", "children")],
                  [Input("button-event-ok", "n_clicks")],
                  [State("intermediate-event-result", "data"),
                   State("input-event-group", "value"),
                   State("checklist-event-pair", "value"),
                   State("radio-event-criteria", "value"),
                   State("checklist-event-email", "value"),
                   State("checklist-event-display", "value")])
    @print_callback(print_function)
    def update_event_result(trigger, records, n_groups, pair_flag, criteria_level, email_flag, hide_flag):
        """Update and display event planner results

        Args:
            trigger: trigger on button click
            records (dict): intermediate data stored in dcc.Store
            n_groups (int): number of groups
            pair_flag (str): option whether to pair participants up
            criteria_level (str): whether criteria is on individual or group level
            email_flag (str): option whether to email results to recipients
            hide_flag (str): option whether to display output results

        Returns:
            3-element tuple

            - list: div result of event planner error (if any)
            - dict: updated style of event planner div
            - list: div result of event planner
        """
        result_error = []
        style = hide_style
        result = []
        if trigger:
            if "df" in records:
                df = decode_df(records["df"])
                event = records["event"]
                result_error, result, style = EventPlanner().process_result(
                    df, event, n_groups, pair_flag, criteria_level, email_flag, hide_flag, style
                )
            else:
                result_error = [return_message["file_not_uploaded"]]
        return html.P(result_error), style, result

    @app.callback([Output("div-rng-item", "style"),
                   Output("div-rng-group", "style"),
                   Output("button-rng-item-ok", "style"),
                   Output("button-rng-group-ok", "style")],
                  [Input("button-rng-item-ok", "n_clicks"),
                   Input("button-rng-group-ok", "n_clicks")],
                  [State("div-rng-item", "style"),
                   State("div-rng-group", "style"),
                   State("button-rng-item-ok", "style"),
                   State("button-rng-group-ok", "style")])
    @print_callback(print_function)
    def update_rng_button_style(trigger_item, trigger_group, item_style, group_style, item_button_style,
        group_button_style
    ):
        """Update style of random generator button

        Args:
            trigger_item: trigger on button click
            trigger_group: trigger on button click
            item_style (dict): current style of item div
            group_style (dict): current style of group div
            item_button_style(dict): current style of item button
            group_button_style (dict): current style of group button

        Returns:
            dict: updated style of item and group button
        """
        if dash.callback_context.triggered:
            ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
            if not item_button_style:
                item_button_style = {}
            if not group_button_style:
                group_button_style = {}
            if ctx == "button-rng-item-ok":
                item_style.update(flex_style)
                item_button_style.update(show_button_style)
                group_style.update(hide_style)
                group_button_style.update(hide_button_style)
            elif ctx == "button-rng-group-ok":
                item_style.update(hide_style)
                item_button_style.update(hide_button_style)
                group_style.update(flex_style)
                group_button_style.update(show_button_style)
        return item_style, group_style, item_button_style, group_button_style

    @app.callback([Output("rng-result-error", "children"),
                   Output("div-rng-result", "style"),
                   Output("div-rng-result", "children")],
                  [Input("button-rng-ok", "n_clicks")],
                  [State("input-rng", "value"),
                   State("input-rng-item", "value"),
                   State("input-rng-group", "value"),
                   State("div-rng-item", "style"),
                   State("div-rng-group", "style"),
                   State("div-rng-result", "style")])
    @print_callback(print_function)
    def update_rng_result(trigger, text, n_items, n_groups, item_style, group_style, style):
        """Update and display random generator results

        Args:
            trigger: trigger on button click
            text (str): input text
            n_items (int): number of items
            n_groups (int): number of groups
            item_style (dict): current style of item div
            group_style (dict): current style of group div
            style (dict): current style of results div

        Returns:
            3-element tuple

            - list: div result of random generator error (if any)
            - dict: updated style of random generator div
            - list: div result of random generator
        """
        result_error = []
        style = hide_style
        result = []
        if trigger:
            task = None
            if item_style["display"] == "flex":
                task = "item"
            elif group_style["display"] == "flex":
                task = "group"
            if text and task:
                result_error, result, style = RandomGenerator().process_result(text, n_items, n_groups, task, style)
            elif not text:
                result_error = [return_message["input_empty"]]
            elif not task:
                result_error = [return_message["rng_task_empty"]]
        return result_error, style, result

    @app.callback([Output("div-wnrs-selection", "style"),
                   Output("div-wnrs-instruction", "style"),
                   Output("div-wnrs-suggestion", "style"),
                   Output("button-wnrs-show-ok", "style"),
                   Output("button-wnrs-instruction-ok", "style"),
                   Output("button-wnrs-suggestion-ok", "style")],
                  [Input("button-wnrs-show-ok", "n_clicks"),
                   Input("button-wnrs-instruction-ok", "n_clicks"),
                   Input("button-wnrs-suggestion-ok", "n_clicks")],
                  [State("div-wnrs-selection", "style"),
                   State("div-wnrs-instruction", "style"),
                   State("div-wnrs-suggestion", "style"),
                   State("button-wnrs-show-ok", "style"),
                   State("button-wnrs-instruction-ok", "style"),
                   State("button-wnrs-suggestion-ok", "style")])
    @print_callback(print_function)
    def update_wnrs_deck_style(trigger_selection, trigger_instruction, trigger_suggestion, selection_style,
        instruction_style, suggestion_style, selection_button_style, instruction_button_style, suggestion_button_style,
    ):
        """Update style of WNRS card selection and card suggestion (visibility)

        Args:
            trigger_selection: trigger on button click
            trigger_instruction: trigger on button click
            trigger_suggestion: trigger on button click
            selection_style (dict): current style of card selection div
            instruction_style (dict): current style of instruction div
            suggestion_style (dict): current style of card suggestion div
            selection_button_style(dict): current style of card selection button
            instruction_button_style (dict): current style of instruction button
            suggestion_button_style (dict): current style of card suggestion button

        Returns:
            dict: updated style of card selection, instruction and card suggestion div and button
        """
        if dash.callback_context.triggered:
            ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
            if not selection_button_style:
                selection_button_style = {}
            if not instruction_button_style:
                instruction_button_style = {}
            if not suggestion_button_style:
                suggestion_button_style = {}
            if ctx == "button-wnrs-show-ok":
                if selection_style["display"] == "inline-block":
                    selection_style.update(hide_style)
                    selection_button_style.update(hide_button_style)
                else:
                    selection_style.update(inline_style)
                    selection_button_style.update(show_button_style)
                instruction_style.update(hide_style)
                instruction_button_style.update(hide_button_style)
                suggestion_style.update(hide_style)
                suggestion_button_style.update(hide_button_style)
            elif ctx == "button-wnrs-instruction-ok":
                if instruction_style["display"] == "inline-block":
                    instruction_style.update(hide_style)
                    instruction_button_style.update(hide_button_style)
                else:
                    instruction_style.update(inline_style)
                    instruction_button_style.update(show_button_style)
                selection_style.update(hide_style)
                selection_button_style.update(hide_button_style)
                suggestion_style.update(hide_style)
                suggestion_button_style.update(hide_button_style)
            elif ctx == "button-wnrs-suggestion-ok":
                if suggestion_style["display"] == "inline-block":
                    suggestion_style.update(hide_style)
                    suggestion_button_style.update(hide_button_style)
                else:
                    suggestion_style.update(inline_style)
                    suggestion_button_style.update(show_button_style)
                selection_style.update(hide_style)
                selection_button_style.update(hide_button_style)
                instruction_style.update(hide_style)
                instruction_button_style.update(hide_button_style)
        return (selection_style, instruction_style, suggestion_style, selection_button_style, instruction_button_style,
                suggestion_button_style)

    @app.callback([Output("input-wnrs-suggestion", "value"),
                   Output("input-wnrs-suggestion2", "value"),
                   Output("wnrs-suggestion-reply", "children")],
                  [Input("button-wnrs-send-ok", "n_clicks")],
                  [State("input-wnrs-suggestion", "value"),
                   State("input-wnrs-suggestion2", "value")])
    @print_callback(print_function)
    def update_wnrs_suggestion_send_email(trigger, card_prompt, additional_info):
        """Send email for WNRS card suggestion

        Args:
            trigger: trigger on button click
            card_prompt (str): input for card prompt
            additional_info (str): input for additional information

        Returns:
            str: feedback for email sent
        """
        reply = ""
        if dash.callback_context.triggered:
            if card_prompt is None or card_prompt.strip() == "":
                reply = return_message["card_not_filled"]
            else:
                status_code = send_email(f"{card_prompt}\n\n{additional_info}")
                if status_code:
                    card_prompt = ""
                    additional_info = ""
                    reply = return_message["email_sent_suggestion"]
                else:
                    reply = return_message["email_fail"]
        return card_prompt, additional_info, reply

    def update_wnrs_button_style_wrapper(deck):
        @app.callback(Output(deck, "style"),
                      [Input(deck, "n_clicks")],
                      [State(deck, "style")])
        @print_callback(print_function)
        def update_wnrs_button_style(trigger, current_style):
            """Update style of selected WNRS decks (button colour indication)

            Args:
                trigger: trigger on button click
                current_style (dict): current style of button

            Returns:
                dict: updated style of button
            """
            if dash.callback_context.triggered:
                if current_style is None:
                    current_style = dict()
                if (
                    "background-color" in current_style
                    and current_style["background-color"] == "#BE9B89"
                ):
                    current_style["background-color"] = "white"
                else:
                    current_style["background-color"] = "#BE9B89"
            return current_style

    all_decks = [
        "Main Deck 1", "Main Deck 2", "Main Deck 3", "Main Deck Final",
        "Bumble x BFF Edition 1", "Bumble x BFF Edition 2", "Bumble x BFF Edition 3",
        "Bumble Bizz Edition 1", "Bumble Bizz Edition 2", "Bumble Bizz Edition 3",
        "Bumble Date Edition 1", "Bumble Date Edition 2", "Bumble Date Edition 3",
        "Cann Edition 1", "Cann Edition 2", "Cann Edition 3",
        "Valentino Edition 1",
        "Honest Dating Edition 1", "Honest Dating Edition 2", "Honest Dating Edition 3",
        "Inner Circle Edition 1", "Inner Circle Edition 2", "Inner Circle Edition 3",
        "Own It Edition 1",
        "Relationship Edition 1", "Relationship Edition 2", "Relationship Edition 3",
        "Race and Privilege Edition 1", "Race and Privilege Edition 2", "Race and Privilege Edition 3",
        "Quarantine Edition 1", "Quarantine Edition 2", "Quarantine Edition 3", "Quarantine Edition Final",
        "Voting Edition 1",
        "Breakup Edition 1", "Breakup Edition Final",
        "Existential Crisis Edition 1",
        "Forgiveness Edition 1",
        "Healing Edition 1",
        "Self-Love Edition 1", "Self-Love Edition Final",
        "Self-Reflection Edition 1",
        "Love Maps 1",
        "Open Ended Questions 1",
        "Rituals of Connection 1",
        "Opportunity 1",
    ]

    for deck in all_decks:
        update_wnrs_button_style_wrapper(deck)

    @app.callback(Output("intermediate-wnrs", "data"),
                  [Input(deck, "style") for deck in all_decks])
    @print_callback(print_function)
    def update_wnrs_list_of_decks(*args):
        """Update list of decks selected

        Args:
            *args (dict): current style of all buttons

        Returns:
            dict: updated style of all buttons
        """
        data = {}
        list_of_deck = []
        for style, deck_name in zip(args, all_decks):
            if style is not None and style["background-color"] == "#BE9B89":
                list_of_deck.append(deck_name)
        if len(list_of_deck):
            wnrs_game = WNRS()
            wnrs_game.initialize_game(list_of_deck)
            data = dict(list_of_deck=list_of_deck, wnrs_game_dict=wnrs_game.__dict__)
        return data

    @app.callback([Output("input-wnrs", "value"),
                   Output("wnrs-prompt", "children"),
                   Output("wnrs-reminder-text", "children"),
                   Output("wnrs-reminder", "children"),
                   Output("wnrs-deck", "children"),
                   Output("wnrs-counter", "children"),
                   Output("wnrs-card", "style"),
                   Output("wnrs-text-back", "children"),
                   Output("wnrs-text-next", "children"),
                   Output("button-wnrs2-back", "style"),
                   Output("button-wnrs2-next", "style")],
                  [Input("button-wnrs-back", "n_clicks"),
                   Input("button-wnrs-next", "n_clicks"),
                   Input("button-wnrs2-back", "n_clicks"),
                   Input("button-wnrs2-next", "n_clicks"),
                   Input("button-wnrs-shuffle-ok", "n_clicks"),
                   Input("intermediate-wnrs", "data"),
                   Input("uploadbutton-wnrs", "contents")],
                  [State("uploadbutton-wnrs", "filename"),
                   State("input-wnrs", "value"),
                   State("wnrs-prompt", "children"),
                   State("wnrs-card", "style"),
                   State("wnrs-text-back", "children"),
                   State("wnrs-text-next", "children"),
                   State("button-wnrs2-back", "style"),
                   State("button-wnrs2-next", "style")])
    @print_callback(print_function)
    def update_wnrs_card(trigger_back, trigger_next, trigger_back2, trigger_next2, trigger_shuffle, data, contents,
                         filename, data2_ser, card_prompt, current_style, text_back, text_next, button_back,
                         button_next):
        """Update underlying data, card content and style

        Args:
            trigger_back: trigger on button click
            trigger_next: trigger on button click
            trigger_back2: trigger on button click
            trigger_next2: trigger on button click
            trigger_shuffle: trigger on button click
            data (dict): data of WNRS object
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded
            data2_ser (str): serialized data of WNRS object
            card_prompt (str/list): current prompt on card
            current_style (dict): current style of card
            text_back (str): current text of words for back button
            text_next (str): current text of words for next button
            button_back (dict): current opacity for back button
            button_next (dict): current opacity for next button

        Returns:
            str, str, str, dict, str, str, str, dict, dict
        """
        card_prompt, card_deck, card_counter, data_new = [card_prompt, "", ""], "", "", {}
        next_card = 0
        if current_style is None:
            current_style = {}
        if dash.callback_context.triggered:
            ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
            data2 = decode_dict(data2_ser)
            if ctx == "intermediate-wnrs":
                if "wnrs_game_dict" not in data:
                    card_prompt[0] = html.P(return_message["card_not_select"])
                else:  # dummy callback
                    data_new = data.copy()
            elif ctx == "uploadbutton-wnrs":
                if "json" not in filename:
                    card_prompt[0] = html.P(return_message["file_not_uploaded_json"])
                else:
                    data = parse_data(contents, filename)
                    data = json.loads(data.decode("utf-8"))
                    try:
                        wnrs_game = WNRS()
                        wnrs_game.load_game(data["list_of_deck"], data["pointer"], data["index"])
                        data_new = dict(
                            list_of_deck=data["list_of_deck"],
                            wnrs_game_dict=wnrs_game.__dict__,
                        )
                    except KeyError:
                        card_prompt[0] = html.P(return_message["wrong_format_json"])
            elif ctx in ["button-wnrs-back", "button-wnrs2-back", "button-wnrs-next", "button-wnrs2-next"]:
                data_new = data2.copy()
                if text_back == "":
                    if ctx.endswith("back"):
                        next_card = -1
                    elif ctx.endswith("next"):
                        next_card = 1
                else:
                    text_back = text_next = ""
                    button_back = button_next = dict(opacity=0)
            elif ctx == "button-wnrs-shuffle-ok":
                data_new = data2.copy()
                next_card = 2
        elif data2_ser is None:
            print("Not triggered")
            data_new = data.copy()
        else:  # initial run
            data2 = decode_dict(data2_ser)
            data_new = data2.copy()

        if len(data_new) > 1:
            wnrs_game = WNRS()
            wnrs_game.load_game_from_dict(data_new["wnrs_game_dict"])
            if next_card == 1:
                card_deck, card_prompt, card_style, card_counter = wnrs_game.get_next_card()
            elif next_card == -1:
                card_deck, card_prompt, card_style, card_counter = wnrs_game.get_previous_card()
            elif next_card == 0:
                card_deck, card_prompt, card_style, card_counter = wnrs_game.get_current_card()
            elif next_card == 2:
                card_deck, card_prompt, card_style, card_counter = wnrs_game.shuffle_remaining_cards()
            data_new["wnrs_game_dict"] = wnrs_game.__dict__
            current_style.update(card_style)
        data_new2 = encode_dict(data_new)
        return [data_new2, *card_prompt, card_deck, card_counter, current_style, text_back, text_next, button_back,
            button_next]

    @app.callback([Output("input-contact-name", "value"),
                   Output("input-contact-email", "value"),
                   Output("input-contact-content", "value"),
                   Output("contact-reply", "children")],
                  [Input("button-contact-ok", "n_clicks")],
                  [State("input-contact-name", "value"),
                   State("input-contact-email", "value"),
                   State("input-contact-content", "value")])
    @print_callback(print_function)
    def update_contact_send_email(trigger, contact_name, contact_email, contact_content):
        """Send email for contact information

        Args:
            trigger: trigger on button click
            contact_name (str): input for contact name
            contact_email (str): input for contact email
            contact_content (str): input for email body

        Returns:
            str: feedback for email sent
        """
        reply = ""
        if dash.callback_context.triggered:
            if contact_name is None or contact_name.strip() == "":
                reply = return_message["email_empty_name"]
            elif contact_email is None or contact_email.strip() == "":
                reply = return_message["email_empty_email"]
            elif not valid_email(contact_email):
                reply = return_message["email_email_valid"]
            elif contact_content is None or contact_content.strip() == "":
                reply = return_message["email_empty_body"]
            else:
                status_code = send_email(f"Name: {contact_name}\n\nEmail: {contact_email}\n\n{contact_content}")
                if status_code:
                    contact_content = ""
                    reply = return_message["email_sent_feedback"]
                else:
                    reply = return_message["email_fail"]
        return contact_name, contact_email, contact_content, reply

    @app.callback(Output("image-canvas", "image_content"),
                  [Input("upload-image", "contents")])
    @print_callback(print_function)
    def update_canvas_image(contents):
        """Update canvas with loaded image

        Args:
            contents: contents of data uploaded, triggers callback

        Returns:
            str: contents of data uploaded
        """
        if dash.callback_context.triggered:
            contents_type, _ = contents.split(";")
            if "image" in contents_type:
                return contents

    @app.callback(Output("image-canvas", "json_objects"),
                  [Input("button-canvas-clear", "n_clicks")])
    @print_callback(print_function)
    def clear_canvas(n_clicks):
        """Clear canvas to blank state

        Args:
            n_clicks: trigger on button click

        Returns:
            str
        """
        strings = ['{"objects":[ ]}', '{"objects":[]}']
        if n_clicks:
            return strings[n_clicks % 2]
        return strings[0]

    @app.callback(Output("knob-canvas", "value"),
                  [Input("button-image-minus", "n_clicks"),
                   Input("button-image-plus", "n_clicks")],
                  [State("knob-canvas", "value")])
    @print_callback(print_function)
    def update_canvas_brush(trigger_minus, trigger_plus, value):
        """Update canvas brush size (line width)

        Args:
            trigger_minus: trigger from button click
            trigger_plus: trigger from button click
            value: value of brush size

        Returns:
            int: updated value of brush size
        """
        ctx = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        if ctx == "button-image-minus":
            value -= 1
        elif ctx == "button-image-plus":
            value += 1
        return value

    @app.callback(Output("image-canvas", "lineWidth"),
                  [Input("knob-canvas", "value")])
    @print_callback(print_function)
    def update_canvas_brush(value):
        """Update canvas brush size (line width)

        Args:
            value: input value of brush size

        Returns:
            int: updated value of brush size
        """
        return value

    @app.callback(Output("image-canvas", "lineColor"),
                  [Input("image-color-picker", "value")])
    @print_callback(print_function)
    def update_canvas_color(value):
        """Update canvas brush colour (line colour)

        Args:
            value: input value of brush colour

        Returns:
            str: updated value of brush colour
        """
        if isinstance(value, dict):
            return value["hex"]
        else:
            return value

    # @app.callback(Output('image-result', 'children'),
    #               [Input('image-canvas', 'json_data')])
    # def update_canvas_result(string):
    #     """Update canvas result
    #
    #     Args:
    #         string: json data of canvas
    #
    #     Returns:
    #         list
    #     """
    #     import numpy as np
    #     from skimage import color, io, filters, measure
    #     from dash_canvas.utils.parse_json import parse_jsonstring
    #     from dash_canvas.utils import array_to_data_url
    #     from dash_canvas.utils.image_processing_utils import modify_segmentation
    #
    #     filename = 'http://www.image.png'
    #     img = io.imread(filename, as_gray=True)
    #     height, width = img.shape
    #     mask = img > 1.2 * filters.threshold_otsu(img)
    #     labs = measure.label(mask)
    #
    #     mask = parse_jsonstring(string, shape=(height, width))
    #     mode = 'merge'  # 'split'
    #     new_labels = modify_segmentation(labs, mask, img=img, mode=mode)
    #     new_labels = np.array(new_labels)
    #     color_labels = color.label2rgb(new_labels)
    #     uri = array_to_data_url(new_labels, dtype=np.uint8)
    #     return uri

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

    @app.callback(Output("tab-content", "children"),
                  [Input("tabs-parent", "value")],
                  [State("tabs-parent", "children"),
                   State("tab-content", "children")])
    @print_callback(print_function)
    def update_output(tab, children, current_content):
        """Update content when tab changes

        Args:
            tab: trigger on tab change
            children (list): list of available tab contents
            current_content (html.Div): current tab content

        Returns:
            html.Div
        """
        available_tabs = [children[idx]["props"]["value"] for idx in range(len(children))]
        if tab not in available_tabs:
            return dcc_loading(violin_plot(), dark_bg=False)
        if tab == "tab-aboutme":
            return about_me_tab(app)
        elif tab == "tab-change":
            return change_tab(app)
        elif tab == "tab-change2":
            return changes_tab(app)
        elif tab == "tab-chat":
            return chat_tab(app)
        elif tab == "tab-trip":
            return trip_tab(app)
        elif tab == "tab-mbti":
            return mbti_tab()
        elif tab == "tab-trade":
            return trade_tab()
        elif tab == "tab-image":
            return image_edit_tab(app)
        elif tab == "tab-contact":
            return contact_tab()
        elif tab == "tab-others":
            return dcc.Location(pathname="/event", id="some_id")
        elif tab == "tab-event":
            return event_tab(app)
        elif tab == "tab-rng":
            return rng_tab()
        elif tab == "tab-wnrs":
            return wnrs_tab(app)
        else:
            return current_content

    app.clientside_callback(
        """
        function(tab_value) {
            if (tab_value === 'tab-aboutme') {
                document.title = 'About Me'
            } else if (tab_value === 'tab-change') {
                document.title = 'Change Calculator'
            } else if (tab_value === 'tab-change2') {
                document.title = 'Change Calculator 2'
            } else if (tab_value === 'tab-chat') {
                document.title = 'Chat Analyzer'
            } else if (tab_value === 'tab-trip') {
                document.title = 'Trip Planner'
            } else if (tab_value === 'tab-mbti') {
                document.title = 'MBTI Personality Test'
            } else if (tab_value === 'tab-trade') {
                document.title = 'Live Trading'
            } else if (tab_value === 'tab-event') {
                document.title = 'Event Planner'
            } else if (tab_value === 'tab-rng') {
                document.title = 'Random Generator'
            } else if (tab_value === 'tab-wnrs') {
                document.title = 'WNRS Card Game'
            } else if (tab_value === 'tab-contact') {
                document.title = 'Contact Me'
            } else if (tab_value === 'tab-image') {
                document.title = 'Image Editing'
            }
        }
        """,
        Output("blank-output", "children"),
        [Input("tabs-parent", "value")],
    )
