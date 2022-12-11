from dash import ctx, dcc, html
from dash.dependencies import Input, Output, State

from components import ChangeCalculator
from components.helper import (
    decode_df,
    get_summary_statistics,
    hide_style,
    inline_style,
    print_callback,
    result_download_button,
    return_message,
    update_when_upload,
)


def register_callbacks(app, print_function):
    @app.callback(
        [
            Output("dropdown-change-worksheet", "options"),
            Output("change-select-worksheet", "style"),
            Output("change-sample-data", "children"),
            Output("change-sample-data", "style"),
            Output("intermediate-change-result", "data"),
        ],
        [
            Input("upload-change", "contents"),
            Input("dropdown-change-worksheet", "value"),
        ],
        [
            State("change-sample-data", "style"),
            State("upload-change", "filename"),
            State("change-select-worksheet", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_change_upload(contents, worksheet, sample_data_style, filename, style):
        """Update change calculator interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            worksheet (str): worksheet of excel file, if applicable, triggers callback
            sample_data_style (dict): current style of sample uploaded data
            filename (str): filename of data uploaded
            style (dict): current style of worksheet selector dropdown

        Returns:
            5-element tuple

            - (list): list of worksheets options
            - (dict): updated style of worksheet selector dropdown
            - (dash_table.DataTable/list): sample of uploaded data
            - (dict): updated style of uploaded data
            - (dict): intermediate data stored in dcc.Store
        """
        return update_when_upload(
            contents, worksheet, sample_data_style, filename, style, ctx.triggered_id
        )

    @app.callback(
        [
            Output("dropdown-change-x", "options"),
            Output("dropdown-change-y", "options"),
        ],
        [Input("intermediate-change-result", "data")],
        prevent_initial_call=True,
    )
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
        if "df" in records:
            df = decode_df(records["df"])
            col_options = [{"label": col, "value": col} for col in df.columns]
            return col_options, col_options
        return [], []

    @app.callback(
        [Output("dropdown-change-x", "value"), Output("dropdown-change-y", "value")],
        [Input("dropdown-change-x", "options"), Input("dropdown-change-y", "options")],
        [State("dropdown-change-x", "value"), State("dropdown-change-y", "value")],
        prevent_initial_call=True,
    )
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
        x_options_list = [opt["label"] for opt in x_options]
        y_options_list = [opt["label"] for opt in y_options]
        if x_value not in x_options_list:
            x_value = None
        if y_value not in y_options_list:
            y_value = None
        return x_value, y_value

    @app.callback(
        [
            Output("change-result-error", "children"),
            Output("change-result-error", "style"),
            Output("div-change-result", "style"),
            Output("change-result", "children"),
            Output("graph-change-result", "figure"),
        ],
        [Input("button-change-ok", "n_clicks")],
        [
            State("intermediate-change-result", "data"),
            State("dropdown-change-x", "value"),
            State("input-change-x", "value"),
            State("dropdown-change-y", "value"),
            State("input-change-y", "value"),
        ],
        prevent_initial_call=True,
    )
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

            - (list): div result of change calculator error (if any)
            - (dict): style of change calculator error (if any)
            - (dict): updated style of change calculator div
            - (list): div result of change calculator
            - (dict): graphical result of change calculator
        """
        result_error = []
        result_error_style = {"color": "red"}
        style = hide_style
        result = []
        fig = {}
        if trigger:
            if (
                "df" in records
                and x_col is not None
                and y_col is not None
                and x_col != y_col
            ):
                result_error = [return_message["scroll_down"]]
                result_error_style = {}
                style = inline_style
                df = decode_df(records["df"])
                df = ChangeCalculator().compute_change(df, x_col, x_max, y_col, y_max)
                result_table = get_summary_statistics(df, [x_col, y_col], dark=False)
                result = [
                    html.H5("Summary Statistics"),
                    result_table,
                    result_download_button(app, df),
                ]
                fig = ChangeCalculator().get_scatter_plot(df, x_col, y_col)
            elif "df" not in records:
                result_error = [return_message["file_not_uploaded"]]
            elif x_col is None or y_col is None:
                result_error = [return_message["change_axis"]]
            elif x_col == y_col:
                result_error = [return_message["change_columns"]]
        return result_error, result_error_style, style, result, fig

    @app.callback(
        [
            Output("dropdown-changes-worksheet", "options"),
            Output("changes-select-worksheet", "style"),
            Output("changes-sample-data", "children"),
            Output("changes-sample-data", "style"),
            Output("intermediate-changes-result", "data"),
        ],
        [
            Input("upload-changes", "contents"),
            Input("dropdown-changes-worksheet", "value"),
        ],
        [
            State("changes-sample-data", "style"),
            State("upload-changes", "filename"),
            State("changes-select-worksheet", "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_changes_upload(contents, worksheet, sample_data_style, filename, style):
        """Update change calculator 2 interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            worksheet (str): worksheet of excel file, if applicable, triggers callback
            sample_data_style (dict): current style of sample uploaded data
            filename (str): filename of data uploaded
            style (dict): current style of worksheet selector dropdown

        Returns:
            5-element tuple

            - (list): list of worksheets options
            - (dict): updated style of worksheet selector dropdown
            - (dash_table.DataTable/list): sample of uploaded data
            - (dict): updated style of uploaded data
            - (dict): intermediate data stored in dcc.Store
        """
        return update_when_upload(
            contents, worksheet, sample_data_style, filename, style, ctx.triggered_id
        )

    @app.callback(
        [
            Output("table-changes", "dropdown"),
            Output("dropdown-changes-identifier", "options"),
        ],
        [Input("intermediate-changes-result", "data")],
        prevent_initial_call=True,
    )
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
        if "df" in records:
            df = decode_df(records["df"])
            col_options = [{"label": col, "value": col} for col in df.columns]
            return dict(column=dict(options=col_options)), col_options
        return {}, []

    @app.callback(
        Output("table-changes", "data"),
        [Input("button-changes-add", "n_clicks")],
        [State("table-changes", "data")],
        prevent_initial_call=True,
    )
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

    @app.callback(
        [
            Output("changes-result-error", "children"),
            Output("changes-result-error", "style"),
            Output("div-changes-result", "style"),
            Output("changes-result", "children"),
            Output("graph-changes-boxplot", "figure"),
            Output("graph-changes-result", "children"),
        ],
        [Input("button-changes-ok", "n_clicks")],
        [
            State("intermediate-changes-result", "data"),
            State("dropdown-changes-identifier", "value"),
            State("table-changes", "data"),
        ],
        prevent_initial_call=True,
    )
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

            - (list): div result of change calculator 2 error (if any)
            - (list): div result of change calculator 2
            - (dict): style of div result of change calculator 2
            - (dict): graphical result of change calculator 2
        """
        result_error = []
        result_error_style = {"color": "red"}
        style = hide_style
        result = []
        fig_box = {}
        graph = []
        if trigger:
            list_of_tuples = [
                (row["column"], row["max"]) for row in data if row["column"]
            ]
            cols = list(dict.fromkeys([row[0] for row in list_of_tuples]))
            if "df" in records and len(list_of_tuples):
                df = decode_df(records["df"])
                df = ChangeCalculator().compute_changes(
                    df, col_identifier, list_of_tuples
                )
                if len(df):
                    result_error = [return_message["scroll_down"]]
                    result_error_style = {}
                    style = inline_style
                    df2 = ChangeCalculator().transpose_dataframe(
                        df, col_identifier, cols
                    )
                    result_table = get_summary_statistics(df, cols)
                    fig_box = ChangeCalculator().get_box_plot(df, cols)
                    instructions_line, fig_line = ChangeCalculator().get_line_plot(
                        app, df2
                    )
                    result = [html.H5("Summary Statistics"), result_table]
                    graph = instructions_line + [
                        dcc.Graph(figure=fig_line, id="graph-changes-line")
                    ]
                elif not len(df):
                    result_error = [return_message["change_numeric"]]
            elif "df" not in records:
                result_error = [return_message["file_not_uploaded"]]
            elif not len(list_of_tuples):
                result_error = [return_message["change_columns_empty"]]
        return result_error, result_error_style, style, result, fig_box, graph

    @app.callback(
        Output("graph-changes-line", "figure"),
        [Input("graph-changes-line", "hoverData")],
        [State("graph-changes-line", "figure")],
    )
    @print_callback(print_function)
    def update_changes_hover(hover_data, figure):
        """Update layouts of plotly graph on hover

        Args:
            hover_data: trigger on hover
            figure (dict): figure for plot

        Returns:
            (dict): updated figure for plot
        """
        for trace in figure["data"]:
            trace["line"]["width"] = 1
            trace["opacity"] = 0.7
        if hover_data:
            trace_index = hover_data["points"][0]["curveNumber"]
            figure["data"][trace_index]["line"]["width"] = 3
            figure["data"][trace_index]["opacity"] = 1
        return figure
