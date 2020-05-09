import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl

from dash.dependencies import Input, Output, State
from tab_layout import about_me_tab, keyboard_tab, trip_tab

app = dash.Dash(__name__)
app.title = 'wow'
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = html.Div([
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


@app.callback(Output('placeholder', 'children'),
              [Input('button_music', 'n_clicks')])
def play(trigger):
    if trigger:
        import base64
        sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
        # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
        encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
        return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)


@app.callback(Output('graph-map', 'children'),
              [Input('graph-map', 'click_lat_lng')],
              [State('input_trip_landmark', 'value'),
               State('graph-map', 'children')])
def click_coord(e, landmark, children):
    if e is not None:
        children.append(
            # Marker icon (dict) can contain iconUrl ("/assets/images/mapbox-icon.png") and iconSize ([25, 25])
            # Marker children (list) can contain dl.Tooltip() and dl.Popup()
            dl.Marker(
                position=[e[0], e[1]],
                children=[
                    dl.Tooltip(landmark),
                ]))
    return children


@app.callback(Output('tab-content', 'children'),
              [Input('tabs-parent', 'value')])
def update_output(tab):
    if tab == 'tab-1':
        return about_me_tab()
    elif tab == 'tab-2':
        return keyboard_tab()
    elif tab == 'tab-3':
        return trip_tab()


if __name__ == '__main__':
    app.run_server(debug=True)
