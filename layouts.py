import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_table

from components.helper import table_css


def main_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])


def app_1():
    return html.Div([
        # Left contents
        html.Div([
            html.Div(
                html.H1(
                    'KJ Wong'
                ),
            ),
            html.Div(
                dcc.Tabs(
                    id='tabs-parent',
                    value=None,
                    vertical=True,
                    parent_className='custom-tabs-parent',
                    className='custom-tabs',
                    children=[
                        dcc.Tab(label='About Me', value='tab-1', className='custom-tab',
                                selected_className='custom-tab-selected'),
                        dcc.Tab(label='Trip Planner', value='tab-2', className='custom-tab',
                                selected_className='custom-tab-selected'),
                        dcc.Tab(label='Change calculator', value='tab-3', className='custom-tab',
                                selected_className='custom-tab-selected'),
                        dcc.Tab(label='Change calculator 2', value='tab-4', className='custom-tab',
                                selected_className='custom-tab-selected'),
                        dcc.Tab(label='Keyboard (WIP)', value='tab-5', className='custom-tab',
                                selected_className='custom-tab-selected'),
                    ],
                    colors={
                        'background': '#202029'
                    },
                    persistence=True,
                    persistence_type='session'
                ),
            )
        ],
            className='sidebar'),

        # Right contents
        html.Div(
            id='tab-content',
            className='contents'
        ),
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
            'Just someone trying to apply what I learn, and believes coding should make our lives easier'
        ),
        html.P(
            'Feel free to write in for any UI/UX suggestion, functionality idea, new use case or bugs encountered!'
        ),
        html.P([
            'Check out my ',
            html.A('linkedin', href='https://www.linkedin.com/in/kayjan/', target='_blank'),
            ' / ',
            html.A('formal website', href='http://kayjan.github.io/', target='_blank')
        ]),
        html.Br(),
        html.Br(),
        html.P([
            'This website is made with Dash, deployed using Gunicorn and hosted on Heroku, '
            'view code documentation on Sphinx ',
            html.A('here', href='/index.html', target='_blank')
        ])
    ])


def get_trip_table():
    """Return the table that displays landmarks information

    Returns:
        (dash_table.DataTable)
    """
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        id='table-trip-landmark',
        columns=[
            dict(name='Landmark', id='Landmark', editable=True),
            dict(name='Street', id='Street'),
            dict(name='lat', id='lat'),
            dict(name='lon', id='lon')
        ],
        data=[],
        style_as_list_view=True,
        style_header=style_header,
        style_cell_conditional=[
            {
                'if': {
                    'column_id': c
                },
                'display': 'none'
            } for c in ['lat', 'lon']
        ],
        style_cell=style_cell,
        css=css
    )


def trip_tab():
    return html.Div([
        header('Trip Planner', 'Shortest distance everrrrr'),
        html.P('Users can fill in multiple destinations and an optimal route will be calculated, '
               'starting and ending from the first destination specified. '
               'This is also known as the Travelling Salesman Problem.'),
        html.Br(),
        html.P('Step 1: Fill in the landmark name (optional)'),
        html.P('Step 2: Click the point on map corresponding to the landmark name'),
        html.P('Step 3: Repeat steps 1 and 2 until all destinations have been entered'),
        html.P('Step 4: Name of landmark can be altered in the table. Try not to use the same landmark name'),
        html.P('Step 5: Click "OK" button to generate the shortest and fastest route!'),
        html.Div([
            # Left item
            html.Div([
                html.P(
                    'Name of landmark:',
                    style={
                        'display': 'inline-block'
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
                get_trip_table(),
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
                            }
                        ),
                    ],
                    type='circle',
                    color='white'
                ),
            ],
                style={
                    'width': '32%',
                    'margin': '2%',
                    'margin-top': '40px',
                    'padding-bottom': '50px',
                },
                className='custom-div'
            ),
            # Right item
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
                    'width': '60%',
                },
                className='custom-div-center'
            ),
        ],
            className='custom-container'
        ),
    ])


def change_tab():
    return html.Div([
        header('Change Calculator', 'Compare changes over two periods'),
        html.P('Users can view summary statistics and plot a scatterplot with marginal histograms of past values '
               '(x axis) against present values (y axis). Users also have the option to download the processed results '
               'with change value into an excel file.'),
        html.Br(),
        html.P('Step 1: Upload a file (.csv, .xls, .xlsx with multiple worksheets supported)'),
        html.P('Step 2: Specify the columns for past values (x axis) and present values (y axis)'),
        html.P('Step 3: Specify the maximum possible value for each column to normalize the column values (optional)'),
        html.P('Step 4: Click "OK" button to generate the results!'),
        html.Div([
            # Left item
            html.Div([
                dcc.Upload(
                    html.P(
                        'Drag and drop files here, or click to upload',
                        style={
                            'margin-bottom': 0
                        }
                    ),
                    id='upload-change',
                    style={
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'padding': '10px'
                    },
                    multiple=False
                ),
                html.P([
                    html.P(
                        'Select worksheet: ',
                        style={
                            'display': 'inline-block',
                            'margin-right': '3px'
                        }
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-change-worksheet',
                            placeholder='Select worksheet',
                            clearable=False,
                            style={
                                'width': '100%',
                                'color': 'black'
                            }
                        ),
                    ],
                        style={
                            'display': 'inline-block',
                            'width': '40%',
                            'verticalAlign': 'middle'
                        }
                    ),
                ],
                    id='change-select-worksheet',
                    style={
                        'display': 'none',
                        'width': '100%',
                        'margin-top': '10px',
                    }
                ),
                html.Div(
                    id='change-sample-data',
                    style={
                        'margin-top': '10px',
                    }
                ),
                html.P([
                    'Select x-axis: ',
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-change-x',
                            placeholder='Select column',
                            clearable=False,
                            style={
                                'width': '100%',
                                'color': 'black'
                            }
                        ),
                    ],
                        style={
                            'display': 'inline-block',
                            'verticalAlign': 'middle',
                            'width': '35%'
                        }
                    ),
                    ' out of ',
                    dcc.Input(
                        id='input-change-x',
                        type='number',
                        min=1,
                        style={'display': 'inline-block', 'width': '20%'}
                    )
                ],
                    style={
                        'margin-top': '10px'
                    }
                ),
                html.P([
                    'Select y-axis: ',
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-change-y',
                            placeholder='Select column',
                            clearable=False,
                            style={
                                'width': '100%',
                                'color': 'black'
                            }
                        ),
                    ],
                        style={
                            'display': 'inline-block',
                            'verticalAlign': 'middle',
                            'width': '35%'
                        }
                    ),
                    ' out of ',
                    dcc.Input(
                        id='input-change-y',
                        type='number',
                        min=1,
                        style={'display': 'inline-block', 'width': '20%'}
                    )
                ],
                    style={
                        'margin-top': '10px'
                    }
                ),
                html.Button(
                    'OK',
                    id='button-change-ok',
                ),
                dcc.Store(
                    id='intermediate-change-result',
                    storage_type='memory'
                ),
                html.Div(
                    id='change-result',
                    style={
                        'margin-top': '30px'
                    }
                ),
            ],
                style={
                    'width': '32%',
                    'margin': '2%',
                    'margin-top': '40px',
                    'padding-bottom': '50px',
                },
                className='custom-div'
            ),
            # Right item
            html.Div([
                html.P('Mouseover for information, highlight to zoom, double click to reset view'),
                html.Div([
                    dcc.Graph(
                        id='graph-change-result'
                    )
                ]),
                html.Div([
                    html.P('Footnote:'),
                    html.P('1. Computation ignores rows where either x or y value is not in numerical format'),
                    html.P('2. Points will be very close to each other (but not overlapping) if two rows have '
                           'identical x and y values, it is recommended to zoom or download the results file'),
                    html.P('3. Interpreting the scatterplot above:'),
                    html.P('** Points above the line represent positive change'),
                    html.P('** Distance from the line represent magnitude of change'),
                    html.P('4. Interpreting the histogram above:'),
                    html.P('** Histogram shows the distribution of values for x and y axis respectively'),
                    html.P('5. Interpreting the summary statistics on the left:'),
                    html.P(
                        '** If median is higher than mean: data is skewed to the left; there is a long tail of low '
                        'scores pulling the mean down'),
                ],
                    style={
                        'margin-left': '20px',
                        'text-align': 'left'
                    }
                ),
            ],
                style={
                    'width': '60%',
                },
                className='custom-div-center'
            ),
        ],
            className='custom-container'
        ),
    ])


def get_changes_table():
    """Return the table used to compare changes across multiple periods

    Returns:
        (dash_table.DataTable)
    """
    style_header, style_cell, style_table, css = table_css()
    return dash_table.DataTable(
        id='table-changes',
        columns=[
            dict(name='Columns to compare', id='column', presentation='dropdown'),
            dict(name='Maximum possible value (integer value, optional)', id='max', type='numeric',
                 on_change={'failure': 'default'}),
        ],
        data=[dict(column='', max='') for i in range(4)],
        editable=True,
        style_as_list_view=True,
        style_header=style_header,
        style_cell=style_cell,
        css=css
    )


def changes_tab():
    return html.Div([
        header('Change Calculator 2', 'Compare changes over multiple periods'),
        html.P('Users can view summary statistics and changes over time on a line plot. '
               'Just minor changes from the other change tab (haha)'),
        html.Br(),
        html.P('Step 1: Upload a file (.csv, .xls, .xlsx with multiple worksheets supported)'),
        html.P('Step 2: Specify column identifier in dropdown option, and columns to compare in the table'),
        html.P('Step 3: Specify the maximum possible value for each column to normalize the column values (optional)'),
        html.P('Step 4: Click "OK" button to generate the results!'),
        html.Div([
            # Left item
            html.Div([
                dcc.Upload(
                    html.P(
                        'Drag and drop files here, or click to upload',
                        style={
                            'margin-bottom': 0
                        }
                    ),
                    id='upload-changes',
                    style={
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'padding': '10px'
                    },
                    multiple=False
                ),
                html.P([
                    html.P(
                        'Select worksheet: ',
                        style={
                            'display': 'inline-block',
                            'margin-right': '3px'
                        }
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-changes-worksheet',
                            placeholder='Select worksheet',
                            clearable=False,
                            style={
                                'width': '100%',
                                'color': 'black'
                            }
                        ),
                    ],
                        style={
                            'display': 'inline-block',
                            'width': '40%',
                            'verticalAlign': 'middle'
                        }
                    ),
                ],
                    id='changes-select-worksheet',
                    style={
                        'display': 'none',
                        'width': '100%',
                        'margin-top': '10px',
                    }
                ),
                html.Div(
                    id='changes-sample-data',
                    style={
                        'margin-top': '10px',
                    }
                ),
                html.Div(
                    id='intermediate-changes-result',
                    style={
                        'display': 'none'
                    }
                ),
            ],
                style={
                    'width': '32%',
                    'margin': '2%',
                    'margin-top': '40px',
                },
                className='custom-div'
            ),
            # Right item
            html.Div([
                html.P([
                    'Column identifier (i.e. Name): ',
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-changes-identifier',
                            placeholder='Select column',
                            clearable=False,
                            style={
                                'width': '100%',
                                'color': 'black'
                            }
                        ),
                    ],
                        style={
                            'display': 'inline-block',
                            'verticalAlign': 'middle',
                            'width': '35%'
                        }
                    )
                ],
                    style={
                        'margin-bottom': '10px'
                    }
                ),
                get_changes_table(),
                html.Button(
                    'Add rows',
                    id='button-changes-add',
                ),
                html.Button(
                    'OK',
                    id='button-changes-ok',
                ),
                html.P([
                    'Footnote:',
                    html.Br(),
                    '1. Computation ignores rows where any column comparison values are not in numerical format',
                    html.Br(),
                    '2. Computation ignores rows where column identifier values are empty',
                    html.Br(),
                    '3. Ensure all column identifier values are unique, if not it will be replaced with running numbers'
                ],
                    style={
                        'margin-top': '10px'
                    }
                )
            ],
                style={
                    'width': '56%',
                    'margin-top': '40px',
                    'margin-bottom': '20px'
                },
                className='custom-div'
            ),
            # Bottom item
            html.Div([
                dcc.Loading(
                    html.P(
                        id='changes-result',
                        style={
                            'display': 'none',
                        },
                        className='custom-div'
                    )
                ),
                html.P(
                    id='div-changes-result',
                    style={
                        'margin-top': '20px'
                    }
                )
            ])
        ],
            className='custom-container'
        ),
    ])


def keyboard_tab():
    return html.Div([
        header('Keyboard', 'Play music on the flyyyyy'),
        html.P('Ideally, users can play the keyboard here. '
               'Im still figuring out how to make it work.'),
        # html.Button('C note', id='button_music')
    ])


def sample_tab():
    return html.Div([
        header('Header', 'Subheader'),
        html.P('Description'),
        html.Br(),
        html.P('Step 1: '),
        html.P('Step 2: '),
        html.Div([
            # Left item
            html.Div([
                # html.P('Left component',),
            ],
                style={
                    'width': '32%',
                    'margin': '2%',
                    'margin-top': '40px',
                    'padding-bottom': '50px',
                },
                className='custom-div'
            ),
            # Right item
            html.Div([
                # html.P('Right component')
            ],
                style={
                    'width': '60%',
                },
                className='custom-div-center'
            ),
        ],
            className='custom-container'
        ),
    ])