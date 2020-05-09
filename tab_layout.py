import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import plotly.graph_objs as go


def header(title, subtitle=None):
    return html.Div([
        html.H2(
            title,
            style={
                'margin-top': '15vh',
            }
        ),
        html.H3(
            subtitle
        ),
        html.H4(
            '————————'
        )
    ])


def about_me_tab():
    return html.Div([
        header('About me'),
        html.P(
            'Just someone trying to apply what I learn, and believes coding should be fun (sometimes frustrating)'
        ),
        html.P([
            'Check out my ',
            html.A('linkedin', href='https://www.linkedin.com/in/kayjan/', target='_blank'),
            ' / ',
            html.A('formal website', href='http://kayjan.github.io/', target='_blank')
        ]),
        html.Br(),
        html.Br(),
        html.P('This website is made with Dash, deployed using Gunicorn and hosted on Heroku')
    ])


def keyboard_tab():
    return html.Div([
        header('Keyboard', 'Play music on the flyyyyy'),
        html.P('Ideally, users can play the keyboard here. '
               'Im still figuring out how to make it work.'),
        # html.Button('C note', id='button_music')
    ])


def get_map():
    mapbox_access_token = 'pk.eyJ1Ijoia2F5amFuIiwiYSI6ImNrOXpicnduZjBkb3ozbXM0OG5neTV4dXIifQ.JTwYhbpDSC_afnc7ndCIrQ'
    return dcc.Graph(
        id='map',
        animate=True,
        figure=go.Figure(
            data=go.Scattermapbox(
                lat=[1.3521, 1.3329],
                lon=[103.8198, 103.7436],
                mode='markers',
            ),
            layout=go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    pitch=0,
                    zoom=10,
                    style='mapbox://styles/kayjan/ck9zh9rx93cwi1im9uan7fl33',
                    center=dict(lat=1.3521, lon=103.8198)
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                clickmode='event+select'
            )
        )
    )


def trip_tab():
    return html.Div([
        header('Trip Planner', 'Shortest distance everrrrr'),
        html.P('Users can fill in the destinations and optimal route will be calculated. '
               'This is obviously still a work in progress. But here is a map.'),
        html.Br(),
        html.P('Step 1: Fill in the landmark name, the place of first and last destination'),
        html.P('Step 2: Using the map: scroll to zoom, drag to move'),
        html.P('Step 3: Once ready, click the point on map corresponding to the landmark name'),
        html.P('Step 4: Repeat until all destinations have been entered'),
        html.P('Step 5: Select route preference (shortest distance / time taken) - WIP'),
        html.P('Step 6: Click "OK" button to generate the route! - WIP'),
        html.Div([
            html.Div([
                html.P(
                    'Name of landmark:',
                    style={
                        'display': 'inline-block',
                        'margin-top': '50px'
                    }
                ),
                dcc.Input(
                    id='input_trip_landmark',
                    type='text',
                    style={
                        'display': 'inline-block',
                        'width': '50%',
                        'margin-left': '10px',
                    }
                )
            ],
                style={
                    'display': 'inline-block',
                    'width': '35%',
                    'text-align': 'left',
                    'vertical-align': 'top',
                },
            ),
            html.Div(
                dl.Map(
                    id='graph-map',
                    style={
                        'height': '400px'},
                    center=[1.3521, 103.8198],
                    zoom=11,
                    children=[
                        dl.TileLayer(id='base-layer'),
                    ]
                ),
                style={
                    'display': 'inline-block',
                    'width': '60%',
                    'vertical-align': 'top',
                },
            ),
        ],
            style={
                'text-align': 'center',
            },
        ),
    ])
