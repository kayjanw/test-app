import numpy as np
import plotly.graph_objects as go
from dash import html


class ChangeCalculator:
    """The ChangeCalculator object contains functions used for
    Change Calculator and Change Calculator 2 tab"""

    @staticmethod
    def remove_string_values(df, col):
        """Remove non-integer values from column(s) in DataFrame

        Args:
            df (pd.DataFrame): input DataFrame
            col (str/list): column(s) to remove non-integer values from

        Returns:
            (pd.DataFrame)
        """
        # Handle string values
        if isinstance(col, str):
            df[col].replace(
                regex=True, to_replace=r"[^0-9.]", value=np.nan, inplace=True
            )
        elif isinstance(col, list):
            for _col in col:
                df[_col].replace(
                    regex=True, to_replace=r"[^0-9.]", value=np.nan, inplace=True
                )
        return df

    @staticmethod
    def remove_null(df, col):
        """Remove null values from column(s) in DataFrame

        Args:
            df (pd.DataFrame): input DataFrame
            col (str/list): column(s) to remove null values from

        Returns:
            (pd.DataFrame)
        """
        # Handle string values
        if isinstance(col, str):
            df.dropna(subset=[col], inplace=True)
        elif isinstance(col, list):
            df.dropna(subset=col, inplace=True)
        return df

    @staticmethod
    def convert_to_float(df, col, col_max):
        """Convert values to float for column(s) in DataFrame, normalize column if necessary

        Args:
            df (pd.DataFrame): input DataFrame
            col (str): column to convert values to float
            col_max (int): maximum value for column, could be None or empty string

        Returns:
            (pd.DataFrame)
        """
        # Convert to float, normalize if necessary
        if col_max:
            df[col] = df[col].astype(float) / col_max * 100
            df[col] = np.round(df[col], 2)
        else:
            df[col] = df[col].astype(float)
        return df

    def compute_change(self, df, x_col, x_max, y_col, y_max):
        """Compute change between two periods

        Performs removing non-integer values, removing null rows and
        conversion of values to float, then adds in 'Change'
        column as difference between y_col and x_col

        Args:
            df (pd.DataFrame): input DataFrame
            x_col (str): column for x-axis
            x_max (int): maximum value for x-axis, could be None or empty string
            y_col (str): column for x-axis
            y_max (int): maximum value for y-axis, could be None or empty string

        Returns:
            (pd.DataFrame)
        """
        df = df.copy()
        df = self.remove_string_values(df, [x_col, y_col])
        df = self.remove_null(df, [x_col, y_col])
        df = self.convert_to_float(df, x_col, x_max)
        df = self.convert_to_float(df, y_col, y_max)
        df["Change"] = df[y_col] - df[x_col]
        return df

    @staticmethod
    def get_scatter_plot(df, x_col, y_col):
        """Get figure for plot

        Adds plotly.graph_objects charts for violin plot, line plot and marginal histograms

        Args:
            df (pd.DataFrame): input DataFrame
            x_col (str): column for x-axis
            y_col (str): column for x-axis

        Returns:
            (dict)
        """
        x_min, x_max = df[x_col].min(), df[x_col].max()
        y_min, y_max = df[y_col].min(), df[y_col].max()
        x_min_limit, x_max_limit = min(0, x_min - 5), max(100, x_max + 5)
        y_min_limit, y_max_limit = min(0, y_min - 5), max(100, y_max + 5)
        trace = go.Violin(
            x=df[x_col],
            y=df[y_col],
            marker={"color": "#202029"},
            text=[
                "<br>".join(
                    [f"{df.columns[idx]}: {x[idx]}" for idx in range(len(df.columns))]
                )
                for x in df.values
            ],
            hoverinfo="text",
            jitter=1,
            points="all",
            line_color="#FFFFFF",
        )
        line = go.Scatter(
            x=[min(x_min, y_min), max(x_max, y_max)],
            y=[min(x_min, y_min), max(x_max, y_max)],
            mode="lines",
            hoverinfo="skip",
        )
        hist_x = go.Histogram(
            x=df[x_col],
            name=x_col + " distribution",
            nbinsx=10,
            yaxis="y2",
            marker={"color": "#202029"},
            hovertemplate="Range: %{x}<br>Total: %{y}<extra></extra>",
        )
        hist_y = go.Histogram(
            y=df[y_col],
            name=y_col + " distribution",
            nbinsy=10,
            xaxis="x2",
            marker={"color": "#202029"},
            hovertemplate="Range: %{y}<br>Total: %{x}<extra></extra>",
            orientation="h",
        )
        layout = dict(
            title="Scatterplot + Histogram of results",
            xaxis=dict(title=x_col, domain=[0, 0.85], range=[x_min_limit, x_max_limit]),
            yaxis=dict(title=y_col, domain=[0, 0.85], range=[y_min_limit, y_max_limit]),
            xaxis2=dict(domain=[0.85, 1]),
            yaxis2=dict(domain=[0.85, 1]),
            hovermode="closest",
            showlegend=False,
            font=dict(
                family="Source Sans Pro",
            ),
        )
        return dict(data=[trace, line, hist_x, hist_y], layout=layout)

    def compute_changes(self, df, col_identifier, list_of_tuples):
        """Compute change between multiple periods

        Performs removing non-integer values, removing null rows and conversion of values to float

        Args:
            df (pd.DataFrame): input DataFrame
            col_identifier (str): column for index
            list_of_tuples (list): data from table that contains tuple of column(s) and their maximum value(s)

        Returns:
            (pd.DataFrame)
        """
        df = df.copy()
        for col, col_max in list_of_tuples:
            df = self.remove_string_values(df, col)
            df = self.remove_null(df, col)
            df = self.convert_to_float(df, col, col_max)
        df = self.remove_null(df, col_identifier)
        return df

    @staticmethod
    def transpose_dataframe(df, col_identifier, cols):
        """Convert long DataFrame to wide DataFrame

        Args:
            df (pd.DataFrame): input DataFrame
            col_identifier (str): column for index, which will be the new DataFrame column names
            cols (list): column names, which will be the new DataFrame index

        Returns:
            (pd.DataFrame)
        """
        df2 = df[cols].transpose()
        if col_identifier:
            df2.columns = df[col_identifier]
        return df2

    @staticmethod
    def get_box_plot(df, cols):
        """Get figure for plot

        Adds plotly.graph_objects charts for box plot, visualizing summary statistics

        Args:
            df (pd.DataFrame): input DataFrame
            cols (list): list of column(s) for results summary

        Returns:
            (dict): graphical result of change calculator 2
        """
        color = [
            "hsl(" + str(h) + ",50%,70%)"
            for h in np.linspace(0, 270, max(len(cols), 7))
        ]
        trace = []
        for idx, col in enumerate(cols):
            trace.append(
                go.Box(
                    y=df[col],
                    name=col,
                    boxpoints="outliers",
                    marker_color=color[idx],
                    hoverinfo="y",
                    hoverlabel=dict(font=dict(family="Source Sans Pro")),
                )
            )
        layout = dict(
            title="Box plot of results",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(type="category"),
            yaxis=dict(
                autorange=True,
                dtick=10,
            ),
            font=dict(family="Source Sans Pro", color="white"),
        )
        return dict(data=trace, layout=layout)

    @staticmethod
    def get_line_plot(app, df2):
        """Get figure for plot

        Adds plotly.graph_objects charts for line plot

        Args:
            df2 (pd.DataFrame): input DataFrame

        Returns:
            2-element tuple

            - (list): instructions for interacting with figure
            - (dict): graphical result of change calculator 2
        """
        trace = []
        instructions = [
            html.Img(src=app.get_asset_url("info.svg")),
            html.Span(["Hover over line to see more information"]),
            html.Span(
                [
                    "Single click on legend to hide entry, "
                    "double click on legend to highlight entry"
                ]
            ),
        ]
        if df2.columns.nunique() < len(df2.columns):
            df2.columns = range(len(df2.columns))
            instructions.append(html.Br())
            instructions.append(
                "Note: Column identifier do not have unique entries, "
                "replaced legend with running numbers"
            )
        for col in df2.columns:
            trace.append(
                go.Scatter(
                    x=list(df2.index),
                    y=df2[col],
                    name=col,
                    mode="lines",
                    line=dict(color="#202029"),
                    text=[
                        f"{col}<br><br>"
                        + "<br>".join(
                            [
                                f"{df2.index[idx]}: {x}"
                                for idx, x in enumerate(df2[col].values)
                            ]
                        )
                    ]
                    * len(df2.index),
                    hoverinfo="text",
                )
            )
        layout = dict(
            title="Line plot of results",
            hovermode="closest",
            hoverdistance=-1,
            xaxis=dict(type="category"),
            font=dict(family="Source Sans Pro", size=16),
        )
        return instructions, dict(data=trace, layout=layout)

    @staticmethod
    def get_parallel_coord(df, col_identifier, list_of_tuples):
        """Get figure for plot

        Adds plotly.graph_objects charts for parallel coordinate plot

        Args:
            df (pd.DataFrame): input DataFrame
            col_identifier (str): column for index
            list_of_tuples (list): data from table that contains tuple of column(s) and their maximum value(s)

        Returns:
            2-element tuple

            - (list): instructions for interacting with figure
            - (dict): graphical result of change calculator 2
        """
        cols = [row[0] for row in list_of_tuples]
        trace = go.Parcoords(
            line_color="#202029",
            # cannot seem to support hover information
            customdata=df[col_identifier],
            dimensions=[
                dict(
                    label=col,
                    values=df[col],
                    range=[
                        np.round(df[col].min() - 5, -1),
                        np.round(df[col].max() + 5, -1),
                    ],
                    tickvals=np.arange(
                        np.round(df[col].min() - 5, -1),
                        np.round(df[col].max() + 5, -1) + 1,
                        10,
                    ),
                )
                for col in cols
            ]
            + [
                dict(
                    label=col_identifier,
                    values=list(range(len(df))),
                    range=[0, len(df)],
                    tickvals=list(range(len(df))),
                    ticktext=df[col_identifier],
                )
            ],
        )
        layout = dict(
            title="Parallel Coordinate plot of results",
            showlegend=True,
            font=dict(
                family="Source Sans Pro",
                size=16,
            ),
        )
        instructions = [
            "Drag along vertical axis line to select a subset of data "
            "(i.e. constrained selection), slide the constrained selection "
            "to toggle the selected range",
            html.Br(),
            "Click anywhere along the vertical axis line to remove constrained selection",
            html.Br(),
            "Slide the axis label to toggle the width between vertical axis lines "
            "or even change the axis order",
        ]
        return instructions, dict(data=[trace], layout=layout)
