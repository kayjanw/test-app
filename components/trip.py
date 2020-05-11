import dash_leaflet as dl
import numpy as np
import requests

try:
    GOOGLE_API_KEY = ENV['GOOGLE_API_KEY']
except NameError:
    import os
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']


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


def get_distance(n):
    matrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?&origins={lat[i]},{lon[i]}&" \
                  f"destinations={lat[j]},{lon[j]}&key={GOOGLE_API_KEY}"
            try:
                page = requests.get(url)
                a = page.json()
                b = a['rows'][0]['elements'][0]['distance']['value']
                matrix[i][j] = b
                print(b)
            except Exception:
                pass
                print(i, j)
            print(matrix)
    return matrix
