import dash
import dash_html_components as html

from dash.dependencies import Input, Output, State
from components.helper import remove_last_point, add_new_point
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


@app.callback([Output('map-trip', 'children'),
               Output('table-trip-landmark', 'data'),
               Output('table-trip-landmark', 'style_table'),
               Output('table-trip-data', 'data')],
              [Input('map-trip', 'click_lat_lng'),
               Input('button-trip-remove', 'n_clicks')],
              [State('input-trip-landmark', 'value'),
               State('map-trip', 'children'),
               State('table-trip-landmark', 'data'),
               State('table-trip-data', 'data')])
def click_coord(e, trigger_remove, landmark, children, data_shown, data_hidden):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'button-trip-remove':
        children, data_shown, data_hidden = remove_last_point(children, data_shown, data_hidden)
    else:
        if e is not None:
            lat, lon = e
            children, data_shown, data_hidden = add_new_point(lat, lon, landmark, children, data_shown, data_hidden)
    if len(data_shown):
        style_table = {
            'width': '80%',
            'margin': '10px 0px 0px 10px',
        }
    else:
        style_table = {
            'display': 'none'
        }
    return children, data_shown, style_table, data_hidden


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
