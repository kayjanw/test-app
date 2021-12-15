import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dash import html
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud as wc

from components.helper import generate_datatable


class ChatAnalyzer:
    """The ChatAnalyzer object contains functions used for Chat Analyzer tab"""

    def __init__(self, fp="", data=None):
        """Initialize class attributes

        Attributes:
            chat_name (str): name of chat
            df (pandas DataFrame): chat data
        """
        if fp:
            with open(fp, "r", encoding="utf8") as f:
                chat = json.load(f)
        else:
            chat = json.loads(data.decode("utf-8"))
        df = pd.DataFrame(chat["messages"])
        df["message_len"] = df["text"].str.len()
        df["date"] = pd.to_datetime(df["date"])
        df["day"] = df["date"].dt.date
        df["hour"] = df["date"].dt.hour

        # Get subset
        message_df = df.query("type == 'message'")
        message_df = message_df[
            message_df.apply(lambda x: isinstance(x["text"], str), axis=1)
        ]  # remove embed links
        text_df = message_df.query("message_len != 0")

        self.chat_name = chat["name"]
        self.df = df
        self.message_df = message_df
        self.text_df = text_df

    def get_message_info_by_sender(self):
        """Get message information by sender

        Returns:
            (list)
        """
        cols = [
            "Sender",
            "Message Count",
            "Sticker Count",
            "Call Count",
            "Avg message length (characters)",
        ]
        if "media_type" in self.message_df.columns:
            sticker_df = self.message_df.query("media_type == 'sticker'")
        else:
            sticker_df = pd.DataFrame(columns=["from"])
        if "action" in self.df.columns:
            call_df = self.df.query("type == 'service' & action == 'phone_call'")
        else:
            call_df = pd.DataFrame(columns=["from", "actor"])

        # Get text_info_df (message count, average message length) from text_df
        text_info_df = self.text_df.groupby(["from"]).agg(
            {"from": "count", "message_len": "mean"}
        )
        text_info_df.columns = [cols[1], cols[4]]
        text_info_df.reset_index(inplace=True)
        text_info_df.rename(columns={"from": cols[0]}, inplace=True)
        text_info_df = text_info_df.round(2)

        # Get sticker_info_df (sticker count) from sticker_df
        sticker_info_df = sticker_df["from"].value_counts().reset_index()
        sticker_info_df.columns = [cols[0], cols[2]]

        # Get call_info_df (call count) from call_df
        call_info_df = call_df.actor.value_counts().reset_index()
        call_info_df.columns = [cols[0], cols[3]]

        # Merge all information
        message_info_df = pd.merge(
            text_info_df.astype(str),
            pd.merge(
                sticker_info_df.astype(str),
                call_info_df.astype(str),
                on=cols[0],
                how="outer",
            ),
            on=cols[0],
            how="outer",
        )
        message_info_df = message_info_df[cols].fillna(0)

        # Generate table for UI
        message_info_table = generate_datatable(
            message_info_df, max_rows=len(message_info_df)
        )
        results = [html.P("Chat Breakdown"), message_info_table]
        return results

    def get_distribution_of_messages_by_hour(self):
        """Get distribution of messages by time sent (grouped on daily level)

        Returns:
            (pandas DataFrame): Data with columns (sender, hour, counts)
        """
        hour_df = self.message_df.groupby(["from", "hour"]).size().reset_index()
        hour_df.columns = ["sender", "hour", "counts"]
        return hour_df

    def get_distribution_of_messages_by_day(self):
        """Get distribution of messages by day

        Returns:
            (pandas DataFrame): Data with columns (sender, day, counts)
        """
        day_df = self.message_df.groupby(["from", "day"]).size().reset_index()
        day_df.columns = ["sender", "day", "counts"]
        return day_df

    def get_time_series_hour_plot(self):
        """Get figure for plot

        Adds plotly.graph_objects charts for line plot

        Returns:
            (dict)
        """
        data = []
        hour_df = self.get_distribution_of_messages_by_hour()
        for sender in hour_df.sender.unique():
            sender_df = hour_df[hour_df.sender == sender]
            sender_df["hour"] = pd.to_datetime(sender_df["hour"], format="%H")
            trace = go.Scatter(
                x=sender_df["hour"],
                y=sender_df["counts"],
                name=sender,
            )
            data.append(trace)

        layout = dict(
            title="Message count by hour",
            margin=dict(l=50, r=50, t=100, b=30),
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickformat="%I:00 %p"),
            font=dict(family="Source Sans Pro", size="15"),
        )
        return dict(data=data, layout=layout)

    def get_time_series_day_plot(self):
        """Get figure for plot

        Adds plotly.graph_objects charts for line plot

        Returns:
            (dict)
        """
        data = []
        day_df = self.get_distribution_of_messages_by_day()
        for sender in day_df.sender.unique():
            sender_df = day_df[day_df.sender == sender]
            trace = go.Scatter(
                x=sender_df["day"],
                y=sender_df["counts"],
                name=sender,
            )
            data.append(trace)

        layout = dict(
            title="Message count by date",
            margin=dict(l=50, r=50, t=100, b=30),
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                font=dict(size="12"),
                rangeslider=dict(visible=True),
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
            ),
            font=dict(family="Source Sans Pro", size="15"),
        )
        return dict(data=data, layout=layout)

    def get_word_cloud(self, max_words=100):
        """Get figure for plot

        Save word cloud image to be displayed

        Returns:
            (html.Img)
        """
        model = CountVectorizer(
            ngram_range=(1, 2),
            max_df=0.01,
            min_df=1,
            max_features=max_words,
            stop_words="english",
            token_pattern="[A-Za-z]+(?=\\s+)",
        )
        document = model.fit_transform(self.text_df["text"])
        word_freq = dict(zip(model.vocabulary_, np.mean(document.toarray(), axis=0)))
        wc2 = wc(max_words=max_words, background_color="white", color_func=None)
        wc_diagram = wc2.generate_from_frequencies(word_freq)
        plt.imshow(wc_diagram, interpolation="bilinear")
