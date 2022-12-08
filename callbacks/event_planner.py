import dash
from dash import html
from dash.dependencies import Input, Output, State

from components import EventPlanner
from components.helper import (
    decode_df,
    encode_df,
    hide_style,
    print_callback,
    return_message,
    update_when_upload,
)


def register_callbacks(app, print_function):
    @app.callback(
        [
            Output("text-event-confirm", "children"),
            Output("text-event-confirm", "style"),
            Output("intermediate-event-result", "data"),
        ],
        [Input("upload-event", "contents")],
        [State("upload-event", "filename")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_event_upload(contents, filename):
        """Update event planner interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded

        Returns:
            3-element tuple

            - (list): message of upload status
            - (dict): style of upload status
            - (str): intermediate data stored in dcc.Store
        """
        upload_message = ""
        upload_message_style = {"color": "red"}
        storage = {}
        if dash.callback_context.triggered:
            _, _, _, _, records = update_when_upload(contents, "", {}, filename, {}, "")
            if "df" in records:
                df = decode_df(records["df"])
                if (
                    df.columns[0] == "Event:"
                    and df.iloc[1, 0] == "Name"
                    and df.iloc[1, 1] == "Email (Optional)"
                ):
                    event = df.columns[1]
                    df = df.iloc[2:, :].rename(columns=df.iloc[1])
                    storage = dict(df=encode_df(df), event=event)
                    upload_message = [return_message["file_uploaded"]]
                    upload_message_style = {}
                else:
                    upload_message = [return_message["wrong_format_demo"]]
            else:
                upload_message = [return_message["wrong_file_type"]]
        return upload_message, upload_message_style, storage

    @app.callback(
        [
            Output("event-result-error", "children"),
            Output("div-event-result", "style"),
            Output("div-event-result", "children"),
        ],
        [Input("button-event-ok", "n_clicks")],
        [
            State("intermediate-event-result", "data"),
            State("input-event-group", "value"),
            State("checklist-event-pair", "value"),
            State("radio-event-criteria", "value"),
            State("checklist-event-email", "value"),
            State("checklist-event-display", "value"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_event_result(
        trigger, records, n_groups, pair_flag, criteria_level, email_flag, hide_flag
    ):
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

            - (list): div result of event planner error (if any)
            - (dict): updated style of event planner div
            - (list): div result of event planner
        """
        result_error = []
        style = hide_style
        result = []
        if trigger:
            if not records:
                result_error = [return_message["file_not_uploaded"]]
            elif "df" in records:
                df = decode_df(records["df"])
                event = records["event"]
                result_error, result, style = EventPlanner().process_result(
                    df,
                    event,
                    n_groups,
                    pair_flag,
                    criteria_level,
                    email_flag,
                    hide_flag,
                    style,
                )
            else:
                result_error = [return_message["file_not_uploaded"]]
        return html.P(result_error), style, result
