import dash
from dash import ctx
from dash.dependencies import Input, Output, State

from common.components.helper import print_callback


def register_callbacks_image_edit(app, print_function):
    @app.callback(
        Output("image-canvas", "image_content"),
        [Input("upload-image", "contents")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_image(contents) -> str:
        """Update canvas with loaded image

        Args:
            contents: contents of data uploaded, triggers callback

        Returns:
            contents of data uploaded
        """
        if dash.callback_context.triggered:
            contents_type, _ = contents.split(";")
            if "image" in contents_type:
                return contents

    @app.callback(
        Output("image-canvas", "json_objects"),
        [Input("button-canvas-clear", "n_clicks")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def clear_canvas(n_clicks) -> str:
        """Clear canvas to blank state

        Args:
            n_clicks: trigger on button click

        Returns:
            (str)
        """
        strings = ['{"objects":[ ]}', '{"objects":[]}']
        if n_clicks:
            return strings[n_clicks % 2]
        return strings[0]

    @app.callback(
        Output("knob-canvas", "value"),
        [
            Input("button-image-minus", "n_clicks"),
            Input("button-image-plus", "n_clicks"),
        ],
        [State("knob-canvas", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_brush_size(trigger_minus, trigger_plus, value) -> int:
        """Update canvas brush size (line width)

        Args:
            trigger_minus: trigger from button click
            trigger_plus: trigger from button click
            value: value of brush size

        Returns:
            updated value of brush size
        """
        if ctx.triggered_id == "button-image-minus":
            value -= 1
        elif ctx.triggered_id == "button-image-plus":
            value += 1
        return value

    @app.callback(
        Output("image-canvas", "lineWidth"),
        [Input("knob-canvas", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_brush(value) -> int:
        """Update canvas brush size (line width)

        Args:
            value: input value of brush size

        Returns:
            updated value of brush size
        """
        return value

    @app.callback(
        Output("image-canvas", "lineColor"),
        [Input("image-color-picker", "value")],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_canvas_color(value) -> str:
        """Update canvas brush colour (line colour)

        Args:
            value: input value of brush colour

        Returns:
            updated value of brush colour
        """
        if isinstance(value, dict):
            return value["hex"]
        else:
            return value

    # @app.callback(Output('image-result', 'children'),
    #               [Input('image-canvas', 'json_data')],
    #               prevent_initial_call=True,
    #               )
    # def update_canvas_result(string):
    #     """Update canvas result
    #
    #     Args:
    #         string: json data of canvas
    #
    #     Returns:
    #         (list)
    #     """
    #     import numpy as np
    #     from skimage import color, io, filters, measure
    #     from dash_canvas.utils.parse_json import parse_jsonstring
    #     from dash_canvas.utils import array_to_data_url
    #     from dash_canvas.utils.image_processing_utils import modify_segmentation
    #
    #     filename = 'http://www.image.png'
    #     img = io.imread(filename, as_gray=True)
    #     height, width = img.shape
    #     mask = img > 1.2 * filters.threshold_otsu(img)
    #     labs = measure.label(mask)
    #
    #     mask = parse_jsonstring(string, shape=(height, width))
    #     mode = 'merge'  # 'split'
    #     new_labels = modify_segmentation(labs, mask, img=img, mode=mode)
    #     new_labels = np.array(new_labels)
    #     color_labels = color.label2rgb(new_labels)
    #     uri = array_to_data_url(new_labels, dtype=np.uint8)
    #     return uri

    # @app.callback(Output('placeholder', 'children'),
    #               [Input('button_music', 'n_clicks')],
    #               prevent_initial_call=True,
    #               )
    # @print_callback(print_function)
    # def update_keyboard(trigger):
    #     if trigger:
    #         import base64
    #         sound_filename = 'assets/Music_Note/sample_sound.wav'  # replace with your own .mp3 file
    #         # sound_filename = 'assets/Music_Note/C.wav'  # replace with your own .mp3 file
    #         encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())
    #         return html.Audio(src=f'data:audio/wav;base64,{encoded_sound.decode()}', controls=False)
