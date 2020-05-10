import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_table


def main_layout():
    return html.Div([
        # Left contents
        html.Div([
            html.Div(
                html.H1([
                    'KJ Wong'
                ],
                    style={
                        'color': 'white'
                    }
                ),
                style={
                    'margin-top': '15vh',
                }
            ),
            html.Div(
                dcc.Tabs(
                    id='tabs-parent',
                    value=None,
                    vertical=True,
                    parent_className='custom-tabs-parent',
                    className='custom-tabs',
                    children=[
                        dcc.Tab(label='About Me', value='tab-1', className='custom-tab'),
                        dcc.Tab(label='Keyboard', value='tab-2', className='custom-tab'),
                        dcc.Tab(label='Trip Planner', value='tab-3', className='custom-tab'),
                    ],
                    colors={
                        'background': '#005b96'
                    },
                    persistence=True,
                    persistence_type='session'
                ),
            )
        ],
            style={
                'position': 'fixed',
                'display': 'inline-block',
                'width': '22vw',
                'height': '97vh',
            },
            className='sidebar'),

        # Right contents
        html.Div(
            id='tab-content',
            style={
                'display': 'inline-block',
                'width': '76vw',
                'margin-left': '22vw',
            }
        ),

        # Hidden contents
        html.Div([
            html.Div(id='placeholder')
        ],
            style={
                'display': 'none'
            }
        )
    ])


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


def trip_tab():
    return html.Div([
        header('Trip Planner', 'Shortest distance everrrrr'),
        html.P('Users can fill in the destinations and optimal route will be calculated. '
               'This is obviously still a work in progress. But here is a map.'),
        html.Br(),
        html.P('Step 1: Fill in the first landmark name, the place of first and last destination'),
        html.P('Step 2: Using the map: scroll to zoom, drag to move'),
        html.P('Step 3: Once ready, click the point on map corresponding to the landmark name'),
        html.P('Step 4: Repeat steps 1 to 3 until all destinations have been entered'),
        html.P('Step 5: Select mode preference (walking / driving)'),
        html.P('Step 6: Click "OK" button to generate the shortest and fastest route!'),
        html.Div([
            html.Div([
                html.P(
                    'Name of landmark:',
                    style={
                        'display': 'inline-block',
                        'margin-top': '50px',
                        'margin-left': '10px'
                    }
                ),
                dcc.Input(
                    id='input-trip-landmark',
                    type='text',
                    style={
                        'display': 'inline-block',
                        'width': '50%',
                        'margin-left': '10px'
                    }
                ),
                dash_table.DataTable(
                    id='table-trip-landmark',
                    columns=[
                        dict(name='Landmark', id='Landmark'),
                        dict(name='Street', id='Street')
                    ],
                    data=[],
                ),
                html.Button(
                    'Remove last landmark',
                    id='button-trip-remove',
                    style={
                        'margin': '10px 0px 0px 10px'
                    }
                )
            ],
                style={
                    'display': 'inline-block',
                    'width': '38%',
                    'text-align': 'left',
                    'vertical-align': 'top'
                },
            ),
            html.Div(
                dl.Map(
                    id='map-trip',
                    style={
                        'height': '400px'},
                    center=[1.3521, 103.8198],
                    zoom=11,
                    children=[
                        dl.TileLayer(),
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

        # Hidden container
        html.Div([
            dash_table.DataTable(
                id='table-trip-data',
                columns=[
                    dict(name='landmark', id='landmark'),
                    dict(name='lat', id='lat'),
                    dict(name='lon', id='lon')
                ],
                data=[],
            ),
        ],
            style={
                'display': 'none'
            }
        )
    ])
