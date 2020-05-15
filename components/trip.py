import dash_html_components as html
import dash_leaflet as dl
import numpy as np
import requests

try:
    GOOGLE_API_KEY = ENV['GOOGLE_API_KEY']
except NameError:
    try:
        import os
        import sys
        GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        os.environ['GRB_LICENSE_FILE'] = sys.path[-1] + '/gurobi.lic'
    except KeyError:
        pass


def remove_last_point_on_table(data):
    data = data[:-1]
    return data


def get_street_name(lat, lon):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={lat},{lon}&key={GOOGLE_API_KEY}'
    page = requests.get(url).json()
    return page['results'][0]['address_components'][1]['long_name']


def add_new_point_on_table(lat, lon, landmark, data):
    # Initialize landmark name if not provided
    if landmark is None or landmark == '':
        landmark = f'Landmark {len(data) + 1}'

    if len(data):
        # Subsequent landmarks
        data.append(
            dict(Landmark=landmark,
                 Street=get_street_name(lat, lon),
                 lat=lat,
                 lon=lon)
        )
    else:
        # If first landmark
        data = [
            dict(Landmark=landmark,
                 Street=get_street_name(lat, lon),
                 lat=lat,
                 lon=lon)
        ]
    return data


def get_style_table(data):
    if len(data):
        style_table = {
            'width': '80%',
            'margin': '10px 0px 0px 10px',
        }
    else:
        style_table = {
            'display': 'none'
        }
    return style_table


def get_map_from_table(data, children):
    children = [children[0]] + [
        # Marker icon (dict) can contain iconUrl ("/assets/images/mapbox-icon.png") and iconSize ([25, 25])
        # Marker children (list) can contain dl.Tooltip() and dl.Popup()
        dl.Marker(
            position=[landmark['lat'], landmark['lon']],
            icon={
                'iconUrl': '/assets/map-icon.svg',
                'iconSize': [38, 100],
                'iconAnchor': [19, 70]
            },
            children=[
                dl.Tooltip(landmark['Landmark']),
            ]) for landmark in data
    ]
    return children


def get_distance_and_duration_from_table(data):
    n = len(data)
    distance_matrix = np.zeros((n, n))
    duration_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?&origins={data[i]['lat']}," \
                      f"{data[i]['lon']}&destinations={data[j]['lat']},{data[j]['lon']}&key={GOOGLE_API_KEY}"
                try:
                    page = requests.get(url).json()
                    distance = page['rows'][0]['elements'][0]['distance']['value']  # in m
                    duration = page['rows'][0]['elements'][0]['duration']['value']  # in sec
                    distance_matrix[i][j] = distance
                    duration_matrix[i][j] = duration
                except Exception as e:
                    raise Exception(f'Cannot get distance data from Google API, error message: {e}')
    return distance_matrix, duration_matrix


def best_route_gurobi(distance_matrix):
    """
    Using gurobi optimiser
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
    model.x = pyEnv.Var(model.N, model.M, within=pyEnv.Binary)  # decision variable x_ij
    model.u = pyEnv.Var(model.N, within=pyEnv.NonNegativeIntegers, bounds=(0, n - 1))  # dummy variable
    model.c = pyEnv.Param(model.N, model.M, initialize=lambda model, i, j: distance_matrix[i - 1][j - 1])

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
        else\
                :
            return model.u[i] - model.u[i] == 0

    model.objective = pyEnv.Objective(rule=min_cost, sense=pyEnv.minimize)
    model.const1 = pyEnv.Constraint(model.M, rule=rule_only_one_edge_in)
    model.rest2 = pyEnv.Constraint(model.N, rule=rule_only_one_edge_out)
    model.rest3 = pyEnv.Constraint(model.U, model.N, rule=rule_no_subtours)

    # Solve
    solver = pyEnv.SolverFactory('gurobi')
    try:
        result = solver.solve(model, tee=False)
    except Exception as e:
        raise Exception(f'Cannot connect to gurobi optimization solver, error message: {e}')

    # Optimal route
    routes_unsorted = []
    for edge in list(model.x.keys()):
        if model.x[edge]() != 0 and model.x[edge]() is not None:
            landmark_from, landmark_to = edge
            routes_unsorted.append((landmark_from-1, landmark_to-1))

    # Sort the route in order
    route_dict = dict(routes_unsorted)
    elem = routes_unsorted[0][0]
    routes = []
    for _ in range(len(routes_unsorted)):
        routes.append((elem, route_dict[elem]))
        elem = route_dict[elem]

    return routes


def best_route_nearest_neighbour(distance_matrix):
    """
    Nearest neighbour heuristic
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


def get_permutation_of_routes(routes_list, landmark):
    permutation = []
    for idx in range(1, len(routes_list)+1):
        routes_list_copy = routes_list.copy()
        routes_list_copy.insert(idx, landmark)
        permutation.append(routes_list_copy)
    return permutation


def get_routes_from_list(routes_list):
    return [(routes_list[idx], routes_list[idx+1]) for idx, _ in enumerate(routes_list[:-1])]


def get_distance_from_routes(routes, distance_matrix):
    distance_km = np.round(np.sum([distance_matrix[route] for route in routes]) / 1000, 2)
    return distance_km


def best_route_nearest_insertion(distance_matrix):
    """
    Nearest insertion heuristic
    """
    idx = 0
    idx_next = distance_matrix[0][1:].argmin() + 1
    visited_landmarks = [idx, idx_next]
    for idx_next in range(len(distance_matrix)):
        best_distance = np.inf
        if idx_next not in visited_landmarks:
            # Get permutation of next insertion
            test_routes = get_permutation_of_routes(visited_landmarks, idx_next)
            for test_route in test_routes:
                # Complete the loop and get shortest distance
                test_route.append(idx)
                test_distance = get_distance_from_routes(get_routes_from_list(test_route), distance_matrix)
                if test_distance < best_distance:
                    best_route = test_route
                    best_distance = test_distance
            visited_landmarks = best_route[:-1]
    visited_landmarks.append(idx)

    # Double check direction of travel
    best_distance = get_distance_from_routes(get_routes_from_list(visited_landmarks), distance_matrix)
    if best_distance > get_distance_from_routes(get_routes_from_list(visited_landmarks[::-1]), distance_matrix):
        visited_landmarks = visited_landmarks[::-1]
    routes = get_routes_from_list(visited_landmarks)
    return routes


def optimiser_pipeline(data):
    if len(data) < 2:
        return html.P('Please input more landmarks')
    try:
        landmarks = [x['Landmark'] for x in data]
        distance_matrix, duration_matrix = get_distance_and_duration_from_table(data)
        try:
            routes = best_route_gurobi(distance_matrix)
        except Exception:
            routes = best_route_nearest_insertion(distance_matrix)
            # routes = best_route_nearest_neighbour(distance_matrix)
        # print(data)
        # print(best_route_gurobi(distance_matrix))
        # print(best_route_nearest_insertion(distance_matrix))
        # print(best_route_nearest_neighbour(distance_matrix))
        distance_km = get_distance_from_routes(routes, distance_matrix)
        duration = np.sum([duration_matrix[route] for route in routes])
        duration_hour = int(np.floor(duration / 3600))
        duration_min = int(np.floor((duration % 3600) / 60))
        answer = [
            html.P(f"Optimal route is {' → '.join([landmarks[i] for i, j in routes])} → {landmarks[0]}"),
            html.P(f"Distance: {distance_km} km"),
            html.P(f"Duration: {duration_hour} hour(s), {duration_min} mins"),
            html.P("This assumes travel mode by driving, and actual duration may depend on traffic conditions")
        ]
    except Exception as e:
        return str(e)
    return answer
