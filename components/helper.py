import dash_leaflet as dl
import numpy as np
import requests

GOOGLE_API_KEY = 'AIzaSyDFVPbpKdZCbDkOFzey_EgCrDqTy6ZqHCs'


def remove_last_point(children, data_shown, data_hidden):
    if len(children) > 1:
        children = children[:-1]
    data_shown = data_shown[:-1]
    data_hidden = data_hidden[:-1]
    return children, data_shown, data_hidden


def get_street_name(lat, lon):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={lat},{lon}&key={GOOGLE_API_KEY}'
    page = requests.get(url).json()
    return page['results'][0]['address_components'][1]['long_name']


def add_new_point(lat, lon, landmark, children, data_shown, data_hidden):
    # Initialize landmark name if not provided
    if landmark is None:
        landmark = f'Landmark {len(data_shown) + 1}'

    if len(data_shown):
        # Subsequent landmarks
        data_shown.append(
            dict(Landmark=landmark,
                 Street=get_street_name(lat, lon))
        )
        data_hidden.append(
            dict(landmark=landmark,
                 lat=lat,
                 lon=lon)
        )
    else:
        # If first landmark
        data_shown = [
            dict(Landmark=landmark,
                 Street=get_street_name(lat, lon))
        ]
        data_hidden = [
            dict(landmark=landmark,
                 lat=lat,
                 lon=lon)
        ]

    # Add custom marker to map
    children.append(
        # Marker icon (dict) can contain iconUrl ("/assets/images/mapbox-icon.png") and iconSize ([25, 25])
        # Marker children (list) can contain dl.Tooltip() and dl.Popup()
        dl.Marker(
            position=[lat, lon],
            children=[
                dl.Tooltip(landmark),
            ]))
    return children, data_shown, data_hidden


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
