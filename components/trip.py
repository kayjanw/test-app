import dash_leaflet as dl
import numpy as np
import requests

try:
    GOOGLE_API_KEY = ENV['GOOGLE_API_KEY']
except NameError:
    import os
    import sys
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    os.environ['GRB_LICENSE_FILE'] = sys.path[-1] + '/gurobi.lic'


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
    routes = []
    for edge in list(model.x.keys()):
        if model.x[edge]() != 0 and model.x[edge]() is not None:
            landmark_from, landmark_to = edge
            routes.append((landmark_from-1, landmark_to-1))

    # Sort the route in order
    route_dict = dict(routes)
    elem = routes[0][0]
    routes_sorted = []
    for _ in range(len(routes)):
        routes_sorted.append((elem, route_dict[elem]))
        elem = route_dict[elem]

    return routes_sorted


def best_route_nn(distance_matrix):
    idx = 0
    visited_landmarks = [0]
    routes_sorted = []
    while len(visited_landmarks) <= len(distance_matrix):
        print(visited_landmarks)
        distances = distance_matrix[idx].copy()
        for visited_landmark in visited_landmarks:
            distances[visited_landmark] = np.inf
        idx_next = distances.argmin()
        routes_sorted.append((idx, idx_next))
        visited_landmarks.append(idx_next)
        idx = idx_next
    return routes_sorted


def optimiser_pipeline(data):
    try:
        landmarks = [x['Landmark'] for x in data]
        distance_matrix, duration_matrix = get_distance_and_duration_from_table(data)
        try:
            routes_sorted = best_route_gurobi(distance_matrix)
        except Exception:
            routes_sorted = best_route_nn(distance_matrix)
        distance_km = np.round(np.sum([distance_matrix[route] for route in routes_sorted]) / 1000, 2)
        duration = np.sum([duration_matrix[route] for route in routes_sorted])
        duration_hour = int(np.floor(duration / 3600))
        duration_min = int(np.floor((duration % 3600) / 60))
        answer = f"Optimal route is {' → '.join([landmarks[i] for i, j in routes_sorted])} → {landmarks[0]} " \
                 f"which is {distance_km} km and will take {duration_hour} hour(s), {duration_min} mins"
    except Exception as e:
        return str(e)
    return answer
