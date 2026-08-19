from dash import no_update
from dash.dependencies import Input, Output, State

from common.components.helper import print_callback, return_message
from main.components.wordle import Wordle
from main.model.wordle import N_GUESSES, N_LETTERS

outputs = []
states = []
for r in range(N_GUESSES):
    for c in range(N_LETTERS):
        outputs.append(Output(f"tile-{r}-{c}", "children"))
        outputs.append(Output(f"tile-{r}-{c}", "style"))
        states.append(State(f"tile-{r}-{c}", "children"))
        states.append(State(f"tile-{r}-{c}", "style"))


def register_callbacks_wordle(app, print_function):
    @app.callback(
        [
            *outputs,
            Output("wordle-state", "data"),
            Output("wordle-output", "children"),
            Output("wordle-guess", "value"),
        ],
        Input("button-wordle", "n_clicks"),
        Input("wordle-guess", "n_submit"),
        [
            State("wordle-guess", "value"),
            State("wordle-state", "data"),
            *states,
        ],
        prevent_initial_call=True,
    )
    @print_callback(print_function)
    def handle_guess(
        n_clicks,
        n_submit,
        guess_word: int,
        state: dict,
        *current_tiles: list[dict[str, str]],
    ):
        """Handle word guess

        Returns:
            tile output, updated state, results, refreshed guess
        """
        if not guess_word:
            return *current_tiles, state, no_update, no_update

        wordle_game = Wordle.from_store(state)
        current_tiles = list(current_tiles)
        msg = ""

        if wordle_game.is_gameover:
            return *current_tiles, state, no_update, no_update

        try:
            results = wordle_game.make_guess(guess_word)
        except ValueError as e:
            return *current_tiles, state, str(e), no_update

        if wordle_game.is_win:
            msg = return_message["wordle_win"]
        elif wordle_game.is_gameover:
            msg = return_message["wordle_lose"].format(word=wordle_game.word)

        n_guesses = len(wordle_game.guesses)
        tile_range = range(
            (n_guesses - 1) * wordle_game.n_letters * 2,
            n_guesses * wordle_game.n_letters * 2,
            2,
        )

        for guess_letter, result_colour, tile_counter in zip(
            wordle_game.guesses[-1], results, tile_range
        ):
            current_tiles[tile_counter] = guess_letter
            current_tiles[tile_counter + 1] = {
                "backgroundColor": result_colour,
                "border": f"2px solid {result_colour}",
                "color": "#ffffff",
            }
        print(wordle_game.to_store())
        return *current_tiles, wordle_game.to_store(), msg, ""
