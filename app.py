import dash
import dash_html_components as html

from dash.dependencies import Input, Output, State
from components.trip import remove_last_point_on_table, add_new_point_on_table, get_map_from_table
from tab_layout import main_layout, about_me_tab, keyboard_tab, trip_tab

app = dash.Dash(__name__)
app.title = 'wow'
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server
app.layout = main_layout()


@app.callback(Output('placeholder', 'children'),
              [Input('button_music', 'n_clicks')])
def play(trigger):
    if trigger:
        import base64
        sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
        # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
        encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
        return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)


@app.callback([Output('table-trip-landmark', 'data'),
               Output('table-trip-landmark', 'style_table'),
               Output('input-trip-landmark', 'value')],
              [Input('map-trip', 'click_lat_lng'),
               Input('button-trip-remove', 'n_clicks')],
              [State('input-trip-landmark', 'value'),
               State('table-trip-landmark', 'data')])
def update_trip_table(e, trigger_remove, landmark, data):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'button-trip-remove':
        data = remove_last_point_on_table(data)
    else:
        if e is not None:
            lat, lon = e
            data = add_new_point_on_table(lat, lon, landmark, data)
    if len(data):
        style_table = {
            'width': '80%',
            'margin': '10px 0px 0px 10px',
        }
    else:
        style_table = {
            'display': 'none'
        }
    return data, style_table, ''



@app.callback(Output('map-trip', 'children'),
              [Input('table-trip-landmark', 'data')],
              [State('map-trip', 'children')])
def update_tripmap(data, children):
    children = get_map_from_table(data, children)
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
