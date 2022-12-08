import dash
from dash import html
from dash.dependencies import Input, Output, State

from components import ChatAnalyzer
from components.helper import (
    generate_datatable,
    hide_style,
    inline_style,
    parse_data,
    print_callback,
    return_message,
)


def register_callbacks(app, print_function):

    # @app.callback(Output('text-chat-loading', 'children'),
    #               [Input('upload-chat', 'contents')])
    # def update_chat_upload_loading(contents):
    #     content = []
    #     if dash.callback_context.triggered:
    #         content = ['Uploading chat...']
    #     return html.P(content, id='text-chat-confirm')

    @app.callback(
        [
            Output("text-chat-confirm", "children"),
            Output("text-chat-confirm", "style"),
            Output("intermediate-chat-result", "data"),
        ],
        [Input("upload-chat", "contents")],
        [State("upload-chat", "filename")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_chat_upload(contents, filename):
        """Update chat analyzer interface when file is uploaded

        Args:
            contents (str): contents of data uploaded, triggers callback
            filename (str): filename of data uploaded

        Returns:
            3-element tuple

            - (list): message of upload status
            - (dict): updated style of upload status
            - (str): intermediate data stored in dcc.Store
        """
        upload_message = ""
        upload_message_style = {"color": "red"}
        storage = {}
        if dash.callback_context.triggered:
            if not filename.endswith(".json"):
                upload_message = [return_message["file_not_uploaded_json"]]
            else:
                data = parse_data(contents, filename)
                try:
                    chat = ChatAnalyzer(data=data)
                    upload_message = [f"Chat uploaded: {chat.chat_name}"]
                    upload_message_style = {}
                    storage = contents
                except AssertionError as e:
                    upload_message = [f"Error: {e}"]
                except KeyError:
                    upload_message = [return_message["wrong_format_json"]]
        return upload_message, upload_message_style, storage

    @app.callback(
        [
            Output("chat-result-error", "children"),
            Output("div-chat-result", "style"),
            Output("chat-result", "children"),
            Output("graph-chat-result-day", "figure"),
            Output("graph-chat-result-hour", "figure"),
            Output("chat-result-wordcloud", "children"),
        ],
        [Input("button-chat-ok", "n_clicks")],
        [State("intermediate-chat-result", "data")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_chat_result(trigger, contents):
        """Update and display chat analyzer results

        Args:
            trigger: trigger on button click
            contents (str): intermediate data stored in dcc.Store

        Returns:
            6-element tuple

            - (list): div result of chat analyzer error (if any)
            - (dict): updated style of chat analyzer div
            - (list): div result of chat analyzer
            - (dict): graphical result 1 of chat analyzer
            - (dict): graphical result 2 of chat analyzer
            - (list): graphical result 3 of chat analyzer
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
                data = parse_data(contents, ".json")
                chat = ChatAnalyzer(data=data)
                processed_df, text_df = chat.process_chat()
                message_info_table = generate_datatable(
                    processed_df, max_rows=len(processed_df), dark=False
                )
                result = [html.H5("Chat Breakdown"), message_info_table]
                fig1 = chat.get_time_series_hour_plot(text_df)
                fig2 = chat.get_time_series_day_plot(text_df)
                fig3 = chat.get_word_cloud(text_df)
        return result_error, style, result, fig1, fig2, fig3
