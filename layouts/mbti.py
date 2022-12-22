from dash import dcc, html

from components.helper import dcc_loading
from layouts.main import content_header


def mbti_tab():
    return html.Div(
        [
            content_header("MBTI Personality Test", "Predict MBTI with writing style"),
            html.Div(
                [
                    html.P(
                        "Users can find out their MBTI personality based on comparing their writing content, specifically "
                        "their choice and phrasing of words, to other users in an existing database of over 8000 people"
                    ),
                    html.Details(
                        [
                            html.Summary(
                                "Click here for more details about the data, processing and modelling steps"
                            ),
                            dcc.Markdown(
                                """
                    ###### Input Distribution
                    > Input data is taken from [Kaggle](https://www.kaggle.com/datasnaek/mbti-type/) and
                    has distribution
                    > - 77% introvert (vs. 23% extrovert)
                    > - 86% intuition (vs. 14% sensing)
                    > - 54% feeling (vs. 46% thinking)
                    > - 60% perceiving (vs. 40% judging)

                    ###### Processing
                    > Processing of training data involves
                    > - Making the words lowercase (so don't worry about your casing)
                    > - Removing URLs `http://` and usernames `@username`
                    > - Removing digits and punctuations
                    > - Remove any mention of MBTI types or the word `mbti`
                    > - Lemmatization of words

                    ###### Modelling (v1)
                    > After processing the text, input data is split into 80% training and 20% testing data in a stratified
                    fashion

                    > Training data has a vocabulary size of **1710 words/bi-grams/tri-grams**

                    > The model used is LightGBM model and 4 different models are trained for each personality trait

                    > Grid search is used to tune each model's hyperparameters based on best *balanced accuracy* score, and
                    > is used with stratified cross validation to handle imbalanced data

                    > Each model, after hyperparameter tuning, is then scored on the held out testing data

                    ###### Modelling (v2)
                    > After processing the text, input data is split into 80% training and 20% testing data in a stratified
                    fashion

                    > Training data has a vocabulary size of **1600 words** with word embedding dimension of 64

                    > The model used is tensorflow neural network model and 4 different models are trained for each
                    > personality trait

                    > Each model, after training for several epochs, is then scored on the held out testing data

                    ###### Results
                    > To interpret the results, accuracy is probability of being correct,
                    > and balanced accuracy is raw accuracy where each sample is weighted according to the inverse
                    > prevalence of its true class, which avoids inflated performance estimates on imbalanced data
                    > * i.e. 70% accuracy means model is correct 70% of the time
                    > * i.e. If model is able to correctly classify actual majority case 70% of the time, and
                    > correctly classify actual minority case 30% of the time, it achieves a balanced accuracy of 50%

                    > The results are
                    > * Introversion-Extroversion Model has Accuracy: 64.4% and Balanced Accuracy: 63.9%
                    > * Intuition-Sensing Model has Accuracy: 65.2% and Balanced Accuracy: 64.4%
                    > * Thinking-Feeling Model has Accuracy: 74.9% and Balanced Accuracy: 75.0%
                    > * Judging-Perceiving Model has Accuracy: 65.4% and Balanced Accuracy: 64.4%
                    > * Please do not take the results too seriously
                    """
                            ),
                        ],
                        title="Expand for details",
                    ),
                    html.Br(),
                    html.P(
                        "Step 1: Fill in the text box with any content (i.e. something you would tweet / short summary of "
                        "yourself)"
                    ),
                    html.P('Step 2: Click "OK" button to generate results!'),
                ],
                className="custom-div-instruction custom-div-left",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Textarea(
                                id="input-mbti",
                                value="",
                                placeholder="Put in your text here, preferably more than 50 words and try not to use "
                                "words that are too common or too complex!",
                            ),
                            html.Div(
                                [html.P(id="text-mbti-words")], style={"float": "right"}
                            ),
                            html.Button("OK", id="button-mbti-ok"),
                            dcc_loading(
                                html.P(id="mbti-result-error", className="color-red"),
                                dark_bg=True,
                            ),
                        ],
                        className="custom-div-small-medium custom-div-space-below custom-div-left custom-div-dark",
                    ),
                    # Result
                    html.Div(
                        [
                            html.Div(id="mbti-results", className="custom-div-center"),
                            dcc_loading(
                                [
                                    dcc.Graph(
                                        id="graph-mbti",
                                        config={
                                            "modeBarButtonsToRemove": [
                                                "zoom2d",
                                                "pan2d",
                                                "select2d",
                                                "lasso2d",
                                                "zoomIn2d",
                                                "zoomOut2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                                "toggleSpikelines",
                                                "hoverClosestCartesian",
                                                "hoverCompareCartesian",
                                            ],
                                        },
                                        style={"display": "none", "height": "100%"},
                                    )
                                ],
                                dark_bg=False,
                            ),
                        ],
                        className="custom-div-center custom-div-half",
                    ),
                ],
                className="custom-container custom-div-space-above",
            ),
        ]
    )
