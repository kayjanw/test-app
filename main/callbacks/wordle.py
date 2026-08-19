from dash import no_update
from dash.dependencies import ALL, Input, Output, State

from common.components.helper import print_callback, return_message
from main.components.wordle import Wordle
from main.model.wordle import N_GUESSES


def register_callbacks_wordle(app, print_function):
    @app.callback(
        [
            Output({"type": "wordle-tile", "id": ALL}, "children"),
            Output({"type": "wordle-tile", "id": ALL}, "style"),
            Output("wordle-state", "data"),
            Output("wordle-output", "children"),
            Output("wordle-guess", "value"),
        ],
        Input("button-wordle", "n_clicks"),
        Input("wordle-guess", "n_submit"),
        [
            State("wordle-guess", "value"),
            State("wordle-state", "data"),
            State("nletters-wordle", "value"),
            State({"type": "wordle-tile", "id": ALL}, "id"),
            State({"type": "wordle-tile", "id": ALL}, "children"),
            State({"type": "wordle-tile", "id": ALL}, "style"),
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_guess(
        n_clicks,
        n_submit,
        guess_word: int,
        state: dict,
        n_letters: int,
        current_tile_ids: list[str],
        current_tiles: list[str | None],
        current_style: list[dict[str, str] | None],
    ):
        """Handle word guess

        Returns:
            tile output, updated state, results, refreshed guess
        """
        if not guess_word:
            return current_tiles, current_style, state, no_update, no_update

        wordle_game = Wordle.from_store(state, n_letters)
        ids_order = [tile["id"] for tile in current_tile_ids]
        msg = ""

        if wordle_game.is_gameover:
            return current_tiles, current_style, state, no_update, no_update

        try:
            results = wordle_game.make_guess(guess_word)
        except ValueError as e:
            return current_tiles, current_style, state, str(e), no_update

        if wordle_game.is_win:
            msg = return_message["wordle_win"]
        elif wordle_game.is_gameover:
            msg = return_message["wordle_lose"].format(word=wordle_game.word)

        n_guesses = len(wordle_game.guesses)
        for tile_count, (guess_letter, result_colour) in enumerate(
            zip(wordle_game.guesses[-1], results)
        ):
            tile_counter = ids_order.index(f"{n_guesses-1}-{tile_count}")
            current_tiles[tile_counter] = guess_letter
            current_style[tile_counter] = {
                "backgroundColor": result_colour,
                "border": f"2px solid {result_colour}",
                "color": "#ffffff",
            }
        print(wordle_game.to_store())
        return current_tiles, current_style, wordle_game.to_store(), msg, ""

    @app.callback(
        Output("wordle-grid", "children"),
        Output("wordle-guess", "maxLength"),
        Output("wordle-guess", "placeholder"),
        [Output({"type": "wordle-row", "id": ALL}, "style")],
        Input("nletters-wordle", "value"),
        State({"type": "wordle-row", "id": ALL}, "style"),
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def update_letters(n_letters, current_style: list[dict[str, str] | None]):
        """Update number of letters for Wordle"""
        new_grid = Wordle.create_grid(N_GUESSES, n_letters)
        placeholder = f"Enter {n_letters} letters"
        row_style = {"grid-template-columns": f"repeat({n_letters}, 1fr)"}
        new_style = []
        for style in current_style:
            new_style.append(style.update(row_style) if style else row_style)
        return new_grid, n_letters, placeholder, new_style
