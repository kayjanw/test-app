from typing import Any, Dict, List

from dash import ctx
from dash.dependencies import Input, Output, State

from components import TripPlanner
from components.helper import print_callback


def register_callbacks(app, print_function):
    @app.callback(
        [
            Output("table-trip-landmark", "data"),
            Output("table-trip-landmark", "style_table"),
            Output("input-trip-landmark", "value"),
        ],
        [
            Input("map-trip", "click_lat_lng"),
            Input("button-trip-remove", "n_clicks"),
            Input("button-trip-reset", "n_clicks"),
        ],
        [State("input-trip-landmark", "value"), State("table-trip-landmark", "data")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_trip_table(
        e, trigger_remove, trigger_reset, landmark: str, data: List[Dict[str, Any]]
    ):
        """Update trip table

        Args:
            e (tuple): trigger on map click
            trigger_remove: trigger on button click
            trigger_reset: trigger on button click
            landmark: name of landmark to be added
            data: data of table that displays landmarks information

        Returns:
            3-element tuple

            - (list): updated data of table that displays landmarks information
            - (dict): style of table that displays landmarks information
            - (str): reset name of next landmark to be added
        """
        if ctx.triggered_id == "button-trip-remove":
            data = TripPlanner().remove_last_point_on_table(data)
        elif ctx.triggered_id == "button-trip-reset":
            data = []
        else:
            if e is not None:
                lat, lon = e
                data = TripPlanner().add_new_point_on_table(lat, lon, landmark, data)
        style_table = TripPlanner().get_style_table(data)
        return data, style_table, ""

    @app.callback(
        Output("map-trip", "children"),
        [Input("table-trip-landmark", "data")],
        [State("map-trip", "children")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_trip_map(data: List[Dict[str, Any]], children: List[Any]):
        """Update trip map to include landmark location pin

        Args:
            data: data of table that displays landmarks information, triggers callback
            children: current map children

        Returns:
            (list): updated map children
        """
        children = TripPlanner().get_map_from_table(data, children)
        return children

    @app.callback(
        Output("trip-result", "children"),
        [Input("button-trip-ok", "n_clicks"), Input("button-trip-reset", "n_clicks")],
        [State("table-trip-landmark", "data")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_trip_results(trigger_ok, trigger_reset, data: List[Dict[str, Any]]):
        """Update and display trip results

        Args:
            trigger_ok: trigger on button click
            trigger_reset: trigger on button click
            data: data of table that displays landmarks information

        Returns:
            (str/list)
        """
        result = ""
        if ctx.triggered_id == "button-trip-ok":
            try:
                result = TripPlanner().optimiser_pipeline(data)
            except IndexError:
                result = TripPlanner().optimiser_pipeline(data)
        elif ctx.triggered_id == "button-trip-reset":
            pass
        return result
