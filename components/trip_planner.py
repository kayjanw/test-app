import dash_leaflet as dl
import numpy as np
import requests

from dash import html


class TripPlanner:
    """The TripPlanner object contains functions used for Trip Planner tab"""

    def __init__(self):
        """Initialize class attributes

        Attributes:
            GOOGLE_API_KEY (str): encrypted Google API key
        """
        try:
            self.GOOGLE_API_KEY = ENV["GOOGLE_API_KEY"]
        except NameError:
            try:
                import os
                import sys

                self.GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
                os.environ["GRB_LICENSE_FILE"] = sys.path[-1] + "/gurobi.lic"
            except KeyError:
                print("No GOOGLE_API_KEY found")
                self.GOOGLE_API_KEY = ""

    @staticmethod
    def remove_last_point_on_table(data):
        """Removes last entry from landmark table

        Args:
            data (list): data of landmark table

        Returns:
            (list)
        """
        data = data[:-1]
        return data

    def get_street_name(self, lat, lon):
        """Get street name from latitude and longitude information, calls Google API

        Return default string if street name is not found

        Args:
            lat (float): latitude information
            lon (float): longitude information

        Returns:
            (str)
        """
        url = (
            f"https://maps.googleapis.com/maps/api/geocode/json?"
            f"address={lat},{lon}"
            f"&key={self.GOOGLE_API_KEY}"
        )
        try:
            page = requests.get(url).json()
        except Exception as e:
            return f"Cannot get distance data from Google API, error message: {e}"
        if page["status"] == "OK":
            return page["results"][0]["address_components"][1]["long_name"]
        else:
            return "Location not found, please select another location."

    def add_new_point_on_table(self, lat, lon, landmark, data):
        """Adds new entry into landmark table

        Args:
            lat (float): latitude information
            lon (float): longitude information
            landmark (str): name of landmark, could be None or empty string
            data (list): data of landmark table

        Returns:
            (list)
        """
        # Initialize landmark name if not provided
        if landmark is None or landmark == "":
            landmark = f"Landmark {len(data) + 1}"

        if len(data):
            # Subsequent landmarks
            data.append(
                dict(
                    Landmark=landmark,
                    Street=self.get_street_name(lat, lon),
                    lat=lat,
                    lon=lon,
                )
            )
        else:
            # If first landmark
            data = [
                dict(
                    Landmark=landmark,
                    Street=self.get_street_name(lat, lon),
                    lat=lat,
                    lon=lon,
                )
            ]
        return data

    @staticmethod
    def get_style_table(data):
        """Return style of landmark table

        Args:
            data (list): data of landmark table

        Returns:
            (dict)
        """
        if len(data):
            style_table = {
                "width": "80%",
                "margin": "10px 0px 0px 10px",
                "overflowX": "auto",
            }
        else:
            style_table = {"display": "none"}
        return style_table

    @staticmethod
    def get_map_from_table(data, children):
        """Adds landmark location pin on map from landmark table

        Args:
            data (list): data of landmark table
            children (list): current map children

        Returns:
            (list): updated map children
        """
        children = [children[0]] + [
            dl.Marker(
                position=[landmark["lat"], landmark["lon"]],
                icon={
                    "iconUrl": "/assets/map-icon.svg",
                    "iconSize": [38, 100],
                    "iconAnchor": [19, 70],
                },
                children=[
                    dl.Tooltip(landmark["Landmark"]),
                ],
            )
            for landmark in data
        ]
        return children

    def get_distance_and_duration_from_table(self, data):
        """Get distance and duration matrix from landmark table, calls Google API

        Args:
            data (list): data of landmark table

        Returns:
            2-element tuple

            - (np.ndarray): distance matrix
            - (np.ndarray): duration matrix
        """
        n = len(data)
        distance_matrix = np.zeros((n, n))
        duration_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    url = (
                        f"https://maps.googleapis.com/maps/api/distancematrix/json?"
                        f"&origins={data[i]['lat']},{data[i]['lon']}"
                        f"&destinations={data[j]['lat']},{data[j]['lon']}"
                        f"&key={self.GOOGLE_API_KEY}"
                    )
                    try:
                        page = requests.get(url).json()
                    except Exception as e:
                        raise Exception(
                            f"Error: Cannot get distance data from Google API, error message: {e}. "
                            f"Please try again later"
                        )
                    if page["rows"][0]["elements"][0]["status"] == "OK":
                        # in m
                        distance = page["rows"][0]["elements"][0]["distance"]["value"]
                        # in sec
                        duration = page["rows"][0]["elements"][0]["duration"]["value"]
                        distance_matrix[i][j] = distance
                        duration_matrix[i][j] = duration
                    else:
                        raise Exception(
                            "Error: Cannot get distance due to invalid location entered"
                        )
        return distance_matrix, duration_matrix

    @staticmethod
    def best_route_gurobi(distance_matrix):
        """Calculates best route using gurobi optimiser

        Args:
            distance_matrix (np.ndarray): inter-distance between locations

        Returns:
            (list): contains tuple of routes
        """
        import pyomo.environ as pyEnv
        import pyutilib.subprocess.GlobalData

        pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False
        n = len(distance_matrix)
        model = pyEnv.ConcreteModel()

        # Variables for landmarks (M, N) and dummy variable (U)
        model.M = pyEnv.RangeSet(n)
        model.N = pyEnv.RangeSet(n)
        model.U = pyEnv.RangeSet(2, n)

        # Decision variable (x_ij), dummy variable (u), cost variable (c)
        # decision variable x_ij
        model.x = pyEnv.Var(model.N, model.M, within=pyEnv.Binary)
        model.u = pyEnv.Var(
            model.N, within=pyEnv.NonNegativeIntegers, bounds=(0, n - 1)
        )  # dummy variable
        model.c = pyEnv.Param(
            model.N,
            model.M,
            initialize=lambda model, i, j: distance_matrix[i - 1][j - 1],
        )

        # Constraints
        def min_cost(model):
            return sum(model.x[i, j] * model.c[i, j] for i in model.N for j in model.M)

        def rule_only_one_edge_in(model, M):
            return sum(model.x[i, M] for i in model.N if i != M) == 1

        def rule_only_one_edge_out(model, N):
            return sum(model.x[N, j] for j in model.M if j != N) == 1

        def rule_no_subtours(model, i, j):
            if i != j:
                return model.u[i] - model.u[j] + model.x[i, j] * n <= n - 1
            else:
                return model.u[i] - model.u[i] == 0

        model.objective = pyEnv.Objective(rule=min_cost, sense=pyEnv.minimize)
        model.const1 = pyEnv.Constraint(model.M, rule=rule_only_one_edge_in)
        model.rest2 = pyEnv.Constraint(model.N, rule=rule_only_one_edge_out)
        model.rest3 = pyEnv.Constraint(model.U, model.N, rule=rule_no_subtours)

        # Solve
        solver = pyEnv.SolverFactory("gurobi")
        try:
            result = solver.solve(model, tee=False)
        except Exception as e:
            raise Exception(
                f"Cannot connect to gurobi optimization solver, error message: {e}"
            )

        # Optimal route
        routes_unsorted = []
        for edge in list(model.x.keys()):
            if model.x[edge]() != 0 and model.x[edge]() is not None:
                landmark_from, landmark_to = edge
                routes_unsorted.append((landmark_from - 1, landmark_to - 1))

        # Sort the route in order
        route_dict = dict(routes_unsorted)
        elem = routes_unsorted[0][0]
        routes = []
        for _ in range(len(routes_unsorted)):
            routes.append((elem, route_dict[elem]))
            elem = route_dict[elem]

        return routes

    @staticmethod
    def best_route_nearest_neighbour(distance_matrix):
        """Calculates best route using nearest neighbour heuristic

        Args:
            distance_matrix (np.ndarray): inter-distance between locations

        Returns:
            (list): contains tuple of routes
        """
        idx = 0
        visited_landmarks = [idx]
        routes = []
        while len(visited_landmarks) <= len(distance_matrix):
            distances = distance_matrix[idx].copy()
            # Replace visited landmarks with distance infinity
            for visited_landmark in visited_landmarks:
                distances[visited_landmark] = np.inf

            # Get next landmark
            idx_next = distances.argmin()

            # Add next landmark and reset variables
            routes.append((idx, idx_next))
            visited_landmarks.append(idx_next)
            idx = idx_next
        return routes

    @staticmethod
    def get_permutation_of_routes(routes_list, landmark):
        """Get permutation of routes with existing routes list and new landmark

        Args:
            routes_list (list): existing routes
            landmark (int): new landmark to visit

        Returns:
            (list): list of list
        """
        permutation = []
        for idx in range(1, len(routes_list) + 1):
            routes_list_copy = routes_list.copy()
            routes_list_copy.insert(idx, landmark)
            permutation.append(routes_list_copy)
        return permutation

    @staticmethod
    def get_routes_from_list(routes_list):
        """Get tuple of routes from existing routes list

        Args:
            routes_list (list): existing routes

        Returns:
            list of tuple
        """
        return [
            (routes_list[idx], routes_list[idx + 1])
            for idx, _ in enumerate(routes_list[:-1])
        ]

    @staticmethod
    def get_distance_from_routes(routes, distance_matrix):
        """Calculates distance from existing routes tuple list

        Args:
            routes (list): list of tuple of existing routes
            distance_matrix (np.ndarray): inter-distance between locations

        Returns:
            (float)
        """
        distance_km = np.round(
            np.sum([distance_matrix[route] for route in routes]) / 1000, 2
        )
        return distance_km

    def best_route_nearest_insertion(self, distance_matrix):
        """Calculates best route using nearest insertion heuristic

        Args:
            distance_matrix (np.ndarray): inter-distance between locations

        Returns:
            (list): contains tuple of routes
        """
        idx = 0
        idx_next = distance_matrix[0][1:].argmin() + 1
        visited_landmarks = [idx, idx_next]
        for idx_next in range(len(distance_matrix)):
            best_distance = np.inf
            if idx_next not in visited_landmarks:
                # Get permutation of next insertion
                test_routes = self.get_permutation_of_routes(
                    visited_landmarks, idx_next
                )
                for test_route in test_routes:
                    # Complete the loop and get shortest distance
                    test_route.append(idx)
                    test_routes = self.get_routes_from_list(test_route)
                    test_distance = self.get_distance_from_routes(
                        test_routes, distance_matrix
                    )
                    if test_distance < best_distance:
                        best_route = test_route
                        best_distance = test_distance
                visited_landmarks = best_route[:-1]
        visited_landmarks.append(idx)

        # Double check direction of travel
        best_routes = self.get_routes_from_list(visited_landmarks)
        best_distance = self.get_distance_from_routes(best_routes, distance_matrix)
        best_routes_inv = self.get_routes_from_list(visited_landmarks[::-1])
        best_distance_inv = self.get_distance_from_routes(
            best_routes_inv, distance_matrix
        )
        if best_distance > best_distance_inv:
            visited_landmarks = visited_landmarks[::-1]
        routes = self.get_routes_from_list(visited_landmarks)
        return routes

    def optimiser_pipeline(self, data):
        """Pipeline to run optimization algorithm

        Args:
            data (list): data of landmark table

        Returns:
            (str/list)
        """
        if len(data) < 2:
            return html.P("Please input more landmarks")
        try:
            landmarks = [x["Landmark"] for x in data]
            (
                distance_matrix,
                duration_matrix,
            ) = self.get_distance_and_duration_from_table(data)
            try:
                routes = self.best_route_gurobi(distance_matrix)
                print(data)
                print(f"Using optimiser: {routes}")
                print(
                    f"Using insertion: {self.best_route_nearest_insertion(distance_matrix)}"
                )
                print(
                    f"Using neighbour: {self.best_route_nearest_neighbour(distance_matrix)}"
                )
            except Exception:
                routes = self.best_route_nearest_insertion(distance_matrix)
            distance_km = self.get_distance_from_routes(routes, distance_matrix)
            duration = np.sum([duration_matrix[route] for route in routes])
            duration_hour = int(np.floor(duration / 3600))
            duration_min = int(np.floor((duration % 3600) / 60))
            answer = [
                html.H5("Shortest Path"),
                html.P(
                    f"Optimal route is "
                    f"{' → '.join([landmarks[i] for i, j in routes])} → {landmarks[0]}"
                ),
                html.P(f"Distance: {distance_km} km"),
                html.P(f"Duration: {duration_hour} hour(s), {duration_min} mins"),
                html.P(
                    "This assumes travel mode by driving, "
                    "and actual duration may depend on traffic conditions"
                ),
            ]
        except Exception as e:
            return str(e)
        return answer
