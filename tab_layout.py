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
                ]),
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
                        dcc.Tab(label='About Me', value='tab-1', className='custom-tab', selected_className='custom-tab-selected'),
                        dcc.Tab(label='Keyboard (WIP)', value='tab-2', className='custom-tab', selected_className='custom-tab-selected'),
                        dcc.Tab(label='Trip Planner', value='tab-3', className='custom-tab', selected_className='custom-tab-selected'),
                    ],
                    colors={
                        'background': '#202029'
                    },
                    persistence=True,
                    persistence_type='session'
                ),
            )
        ],
            style={
                'height': '100vh'
            },
            className='sidebar'),

        # Right contents
        html.Div(
            id='tab-content',
            className='contents'
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
        html.P('Users can fill in the destinations and optimal route will be calculated, '
               'starting and ending from the first destination specified. '
               'This is also known as the Travelling Salesman Problem.'),
        html.Br(),
        html.P('Step 1: Fill in the landmark name (optional)'),
        html.P('Step 2: Click the point on map corresponding to the landmark name'),
        html.P('Step 3: Repeat steps 1 and 2 until all destinations have been entered'),
        html.P('Step 4: Name of landmark can be altered in the table. Try not to use the same landmark name'),
        html.P('Step 5: Click "OK" button to generate the shortest and fastest route!'),
        html.Div([
            html.Div([
                html.P(
                    'Name of landmark:',
                    style={
                        'display': 'inline-block',
                        'margin': 0,
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
                        dict(name='Landmark', id='Landmark', editable=True),
                        dict(name='Street', id='Street'),
                        dict(name='lat', id='lat'),
                        dict(name='lon', id='lon')
                    ],
                    data=[],
                    style_as_list_view=True,
                    style_header={
                        'fontWeight': 'bold',
                        'textAlign': 'left'
                    },
                    style_cell_conditional=[
                        {
                            'if': {
                                'column_id': c
                            },
                            'display': 'none'
                        } for c in ['lat', 'lon']
                    ],
                    style_cell={
                        'background-color': 'transparent',
                        'color': 'white',
                        'font-family': 'Source Sans Pro',
                        'font-size': 13,
                        'textAlign': 'left'
                    },
                    css=[{
                        'selector': 'tr:hover',
                        'rule': 'background-color: black; color: white'
                    }, {
                        'selector': 'td.cell--selected *, td.focused *',
                        'rule': 'background-color: black !important;'
                                'color: white !important;'
                                'text-align: left;'
                    }]
                ),
                html.Button(
                    'Remove last landmark',
                    id='button-trip-remove',
                ),
                html.Button(
                    'Reset all landmarks',
                    id='button-trip-reset',
                ),
                html.Br(),
                html.Button(
                    'OK',
                    id='button-trip-ok',
                ),
                dcc.Loading(
                    children=[
                        html.Div(
                            id='trip-results',
                            style={
                                'margin-top': '30px',
                                'margin-right': '10px',
                                'margin-left': '-10px'
                            }
                        ),
                    ],
                    type='circle',
                    color='white'
                ),
            ],
                style={
                    'display': 'inline-block',
                    'width': '32%',
                    'margin': '2%',
                    'margin-top': '40px',
                    'padding': '2%',
                    'padding-bottom': '50px',
                    'text-align': 'left',
                    'vertical-align': 'top'
                },
                className='custom-div'
            ),
            html.Div([
                html.P('Scroll to zoom, drag to move'),
                dl.Map(
                    id='map-trip',
                    style={
                        'height': '400px',
                    },
                    center=[1.3521, 103.8198],
                    zoom=11,
                    children=[
                        dl.TileLayer(),
                    ]
                )],
                style={
                    'display': 'inline-block',
                    'width': '60%',
                    'vertical-align': 'top'
                },
            ),
        ],
            style={
                'margin-top': '20px',
                'margin-bottom': '20px',
                'text-align': 'center'
            }
        ),
    ])
