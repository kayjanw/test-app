import json
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud as wc

from components.helper import create_fig_from_diagram

pd.options.mode.chained_assignment = None


class ChatAnalyzer:
    """The ChatAnalyzer object contains functions used for Chat Analyzer tab"""

    def __init__(self, fp: str = "", data: Optional[str] = None):
        """Initialize class attributes

        Args:
            fp (str): file path of data, default to empty string
            data (str): data, default to None

        Attributes:
            chat_name (str): name of new columns generated
            df (pd.DataFrame): all chat data
        """
        assert fp or data, "Please specify file name or pass in data"
        if fp:
            with open(fp, "r", encoding="utf8") as f:
                chat = json.load(f)
        else:
            chat = json.loads(data.decode("utf-8"))
        df = pd.DataFrame(chat["messages"])
        assert len(df), "No messages found"

        # Misc processing
        main_cols = ["type", "date", "from", "text"]
        misc_cols = ["edited", "media_type", "photo"]
        for col in misc_cols:
            if col not in df:
                df[col] = np.nan
        if "actor" in df:
            df["from"] = np.where(df["from"].isnull(), df["actor"], df["from"])
        if "duration_seconds" in df:
            df = df[~((df["type"] == "service") & df["duration_seconds"].isnull())]
        if "location_information" in df:
            df = df[df["location_information"].isnull()]
        df = df[main_cols + misc_cols].copy()
        df["message_len"] = df["text"].str.len()
        df["date"] = pd.to_datetime(df["date"])
        df["day"] = df["date"].dt.date
        df["hour"] = df["date"].dt.hour

        self.chat_name = chat["name"]
        self.df = df

    def process_chat(self):
        """Process chat to get statistics and intermediate message data

        Returns:
        2-element tuple

        - process_text (pd.DataFrame): statistics of chat
        - text_df (pd.DataFrame): text message data
        """
        # Filtering
        message_df = self.df[(self.df["type"] == "message")]
        call_df = self.df[self.df["type"] == "service"]

        text_df = message_df[
            message_df["media_type"].isnull() & message_df["photo"].isnull()
        ]
        photo_df = message_df[
            message_df["media_type"].isnull() & ~message_df["photo"].isnull()
        ]
        video_df = message_df[message_df["media_type"] == "video_file"]
        voice_message_df = message_df[message_df["media_type"] == "voice_message"]
        video_message_df = message_df[message_df["media_type"] == "video_message"]
        sticker_df = message_df[message_df["media_type"] == "sticker"]
        gif_df = message_df[message_df["media_type"] == "animation"]

        # Processing
        text_df = text_df[
            text_df.apply(lambda x: isinstance(x["text"], str), axis=1)
        ]  # remove embed links

        # Combine results
        processed_df = (
            text_df.groupby("from")
            .agg({"from": "count", "edited": "count", "message_len": "mean"})
            .round({"message_len": 1})
            .rename(
                columns={
                    "from": "Message Count",
                    "edited": "Edited Message Count",
                    "message_len": "Avg message length (characters)",
                }
            )
        )
        list_of_df = [
            (sticker_df, ["Sticker Count"]),
            (gif_df, ["Gif Count"]),
            (call_df, ["Call Count"]),
            (photo_df, ["Photo Count"]),
            (video_df, ["Video Count"]),
            (voice_message_df, ["Voice Message Count"]),
            (video_message_df, ["Video Message Count"]),
        ]
        for df_small, col in list_of_df:
            if len(df_small):
                df_small_tmp = df_small.groupby("from").agg({"from": "count"})
                df_small_tmp.columns = col
                processed_df = processed_df.join(df_small_tmp, on="from")
        processed_df = processed_df.T.reset_index().rename(columns={"index": ""})

        return processed_df, text_df

    @staticmethod
    def get_distribution_of_messages_by_hour(text_df: pd.DataFrame) -> pd.DataFrame:
        """Get distribution of messages by time sent (grouped on daily level)

        Args:
            text_df: text message data

        Returns:
            (pd.DataFrame): data with columns (sender, hour, counts)
        """
        hour_df = text_df.groupby(["from", "hour"]).size().reset_index()
        hour_df.columns = ["sender", "hour", "counts"]
        return hour_df

    @staticmethod
    def get_distribution_of_messages_by_day(text_df: pd.DataFrame) -> pd.DataFrame:
        """
        Get distribution of messages by day

        Args:
            text_df: text message data

        Returns:
            data with columns (sender, day, counts)
        """
        day_df = text_df.groupby(["from", "day"]).size().reset_index()
        day_df.columns = ["sender", "day", "counts"]
        return day_df

    def get_time_series_hour_plot(
        self, text_df: pd.DataFrame, template: str
    ) -> go.Figure:
        """Get figure for plot
        Adds plotly.graph_objects charts for line plot

        Args:
            text_df: all chat data where type is message
            template: template of plot

        Returns:
            Message count by hour plot
        """
        data = []
        hour_df = self.get_distribution_of_messages_by_hour(text_df)
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
            font=dict(family="Source Sans Pro", size=15),
        )

        fig = go.Figure(dict(data=data, layout=layout))
        fig.update_layout(template=template)
        return fig

    def get_time_series_day_plot(
        self, text_df: pd.DataFrame, template: str
    ) -> go.Figure:
        """Get figure for plot
        Adds plotly.graph_objects charts for line plot

        Args:
            text_df: text message data
            template: template of plot

        Returns:
            Message count by date plot
        """
        data = []
        day_df = self.get_distribution_of_messages_by_day(text_df)
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
                tickfont=dict(size=12),
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
            font=dict(family="Source Sans Pro", size=15),
            template=template,
        )

        fig = go.Figure(dict(data=data, layout=layout))
        fig.update_layout(template=template)
        return fig

    @staticmethod
    def get_word_cloud(
        text_df: pd.DataFrame, max_words: int = 100, plotly: bool = True
    ) -> html.Img:
        """Get figure for plot
        Adds plotly.graph_objects charts for word cloud plot

        Args:
            text_df: text message data
            max_words: maximum words to consider in word cloud
            plotly: whether image should be returned to console, defaults to True (hidden from console)

        Returns:
            Word cloud image
        """
        image = html.Img()
        try:
            model = CountVectorizer(
                ngram_range=(1, 2),
                max_df=0.01,
                min_df=1,
                max_features=max_words,
                stop_words="english",
                token_pattern="[A-Za-z]+(?=\\s+)",
            )
            document = model.fit_transform(text_df["text"])
            word_freq = dict(
                zip(model.vocabulary_, np.mean(document.toarray(), axis=0))
            )
            wc2 = wc(
                max_words=max_words, background_color="white", height=500, width=1000
            )
            wc_diagram = wc2.generate_from_frequencies(word_freq)

            def grey_color_func(
                word, font_size, position, orientation, random_state=None, **kwargs
            ):
                return "hsl(0, 0%%, %d%%)" % np.random.randint(0, 60)

            if plotly:
                fig, axs = plt.subplots(1, 1, figsize=(10, 5), squeeze=False)
                axs = axs.ravel()
                axs[0].imshow(
                    wc_diagram.recolor(color_func=grey_color_func, random_state=3),
                    interpolation="bilinear",
                )
                axs[0].axis("off")
                axs[0].set_title("Word Cloud of Messages")
                image = create_fig_from_diagram(
                    fig, "wordcloud", className="custom-div-full"
                )
            else:
                plt.imshow(
                    wc_diagram.recolor(color_func=grey_color_func, random_state=3),
                    interpolation="bilinear",
                )
        except ValueError:
            pass

        return image
