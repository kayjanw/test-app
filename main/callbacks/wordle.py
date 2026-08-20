from dash import ctx, no_update
from dash.dependencies import ALL, Input, Output, State

from common.components.helper import print_callback
from main.components.wordle import Wordle, create_grid, get_tile_style
from main.model.wordle import N_GUESSES


def register_callbacks_wordle(app, print_function):
    @app.callback(
        [
            # Change on n_clicks, n_submit
            Output({"type": "wordle-tile", "id": ALL}, "children"),
            Output({"type": "wordle-tile", "id": ALL}, "style"),
            Output("wordle-state", "data"),
            Output("wordle-output", "children"),
            Output("wordle-guess", "value"),
            # Change when n_letters change
            Output("wordle-grid", "children"),
            Output("wordle-guess", "maxLength"),
            Output("wordle-guess", "placeholder"),
        ],
        Input("submit-wordle", "n_clicks"),
        Input("wordle-guess", "n_submit"),
        Input("redo-wordle", "n_clicks"),
        Input("switch-wordle", "n_clicks"),
        [
            State("wordle-guess", "value"),
            State("wordle-state", "data"),
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
        n_redo,
        n_switch,
        guess_word: int,
        state: dict,
        current_tile_ids: list[dict[str, str]],
        current_tiles: list[str | None],
        current_style: list[dict[str, str] | None],
    ):
        """Handle word guess and n_letter changes

        Returns:
            for n_click, n_submit: tile output, updated state, results, refreshed guess
            for n_letters change: grid layout, updated input,
        """
        triggered_id = ctx.triggered_id
        guess_results = current_tiles, current_style, no_update, no_update, no_update
        n_letters_results = no_update, no_update, no_update

        n_letters = len(state["word"])
        if triggered_id in ["switch-wordle", "redo-wordle"]:
            if triggered_id == "switch-wordle":
                n_letters += 1 if n_letters == 5 else -1
            placeholder = f"Enter {n_letters} letters"

            # Reset existing game
            new_grid = create_grid(N_GUESSES, n_letters)
            wordle_game = Wordle(n_letters=n_letters)
            n_letters_results = new_grid, n_letters, placeholder
        else:
            # Play game
            wordle_game = Wordle.from_store(state, n_letters)
            ids_order = [tile["id"] for tile in current_tile_ids]

            if not guess_word or wordle_game.is_gameover:
                return *guess_results, *n_letters_results

            try:
                results = wordle_game.make_guess(guess_word)
            except ValueError as e:
                return (
                    current_tiles,
                    current_style,
                    no_update,
                    str(e),
                    no_update,
                    *n_letters_results,
                )

            n_guesses = len(wordle_game.guesses)
            for tile_count, (guess_letter, result_colour) in enumerate(
                zip(wordle_game.guesses[-1], results)
            ):
                tile_counter = ids_order.index(f"{n_guesses-1}-{tile_count}")
                current_tiles[tile_counter] = guess_letter
                current_style[tile_counter] = get_tile_style(result_colour)
        print(wordle_game.to_store())
        return (
            current_tiles,
            current_style,
            wordle_game.to_store(),
            wordle_game.state,
            "",
            *n_letters_results,
        )
