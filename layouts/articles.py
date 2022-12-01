import dash_bootstrap_components as dbc

from dash import html

from layouts.main import content_header

color_productivity = "lightblue"
color_dashboard = "blue"
color_ds = "red"
color_best_practices = "green"
color_se = "yellow"

# Productivity
article_coursera = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Productivity"),
                    html.H5("5 Tips After Completing 100 Coursera Courses"),
                    html.P("Reflections on my e-learning journey."),
                ],
            ),
        ],
        className=f"zoom background-{color_productivity}",
    ),
    href="https://medium.com/towards-data-science/5-tips-after-completing-100-coursera-courses-1ee5a35e72a4",
    target="_blank",
)

# Dashboard
article_dashboard = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Dashboard"),
                    html.H5("Advancing to Professional Dashboard with Python, using Dash"),
                    html.P("Advanced ways to enhance initial skeleton code."),
                ],
            ),
        ],
        className=f"zoom background-{color_dashboard}",
    ),
    href="https://medium.com/towards-data-science/advancing-to-professional-dashboard-with-python-using-dash-and-plotly-1e8e5aa4c668",
    target="_blank",
)

# Data Science
article_reinforcement_learning = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Data Science"),
                    html.H5("6 Reinforcement Learning Algorithms Explained"),
                    html.P("Introduction to reinforcement learning terminologies, basics, and concepts."),
                ],
            ),
        ],
        className=f"zoom background-{color_ds}",
    ),
    href="https://medium.com/towards-data-science/6-reinforcement-learning-algorithms-explained-237a79dbd8e",
    target="_blank",
)

article_ensemble = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Data Science"),
                    html.H5("CatBoost vs. LightGBM vs. XGBoost"),
                    html.P("Which is the best algorithm?"),
                ],
            ),
        ],
        className=f"zoom background-{color_ds}",
    ),
    href="https://medium.com/towards-data-science/catboost-vs-lightgbm-vs-xgboost-c80f40662924",
    target="_blank",
)

# Coding Best Practices
article_best_practices = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Coding Best Practices"),
                    html.H5("3 Tips for Writing Clean Codes Beyond Coding Best Practices"),
                    html.P("Write elegant, modular, understandable, and maintainable codes."),
                ],
            ),
        ],
        className=f"zoom background-{color_best_practices}",
    ),
    href="https://medium.com/towards-data-science/3-tips-for-writing-clean-codes-beyond-coding-best-practices-c53b04120c3",
    target="_blank",
)

article_programming = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Coding Best Practices"),
                    html.H5("How to Learn New Programming Languages Easily"),
                    html.P("Pick up any new programming language — with Python, Java, and Go examples."),
                ],
            ),
        ],
        className=f"zoom background-{color_best_practices}",
    ),
    href="https://medium.com/towards-data-science/how-to-learn-new-programming-languages-easily-1e6e29d3898a",
    target="_blank",
)

article_sphinx = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Coding Best Practices"),
                    html.H5("Advanced Code Documentation Beyond Comments and Docstrings"),
                    html.P("Use Sphinx and Read the Docs for a user-friendly interface to understand codebase — even for non-technical users."),
                ],
            ),
        ],
        className=f"zoom background-{color_best_practices}",
    ),
    href="https://medium.com/towards-data-science/advanced-code-documentation-beyond-comments-and-docstrings-2cc5b2ace28a",
    target="_blank",
)

# Software Engineering
article_bigtree = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Python Tree Implementation with BigTree"),
                    html.P("Integrating trees with Python lists, dictionaries, and pandas DataFrames."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/python-tree-implementation-with-bigtree-13cdabd77adc",
    target="_blank",
)

article_logging = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Basic to Advanced Logging with Python in 10 Minutes"),
                    html.P("Logging crash course with common logging issues addressed."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/basic-to-advanced-logging-with-python-in-10-minutes-631501339650",
    target="_blank",
)

article_lists = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("3 Data Structures for Faster Python Lists"),
                    html.P("Choose your lists wisely."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/3-data-structures-for-faster-python-lists-f29a7e9c2f92",
    target="_blank",
)

article_pytest = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Pytest with Marking, Mocking, and Fixtures in 10 Minutes"),
                    html.P("Write robust unit tests with Python pytest."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/pytest-with-marking-mocking-and-fixtures-in-10-minutes-678d7ccd2f70",
    target="_blank",
)

article_unittest = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Unit Testing with Mocking in 10 Minutes"),
                    html.P("Test your codebase effectively with the built-in unittest Python package."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://towardsdatascience.com/unit-testing-with-mocking-in-10-minutes-e28feb7e530",
    target="_blank",
)

article_fastapi = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Implementing FastAPI in 10 Minutes"),
                    html.P("Develop, test, and use your custom API."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/implementing-fastapi-in-10-minutes-d161cdd7c075",
    target="_blank",
)

article_multithreading = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Multithreading and Multiprocessing in 10 Minutes"),
                    html.P("Multitasking made easy with Python examples."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/multithreading-and-multiprocessing-in-10-minutes-20d9b3c6a867",
    target="_blank",
)

article_mlflow = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Experiment Tracking with MLflow in 10 Minutes"),
                    html.P("Managing Machine Learning Lifecycle made easy — explained with Python examples."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/experiment-tracking-with-mlflow-in-10-minutes-f7c2128b8f2c",
    target="_blank",
)

article_airflow = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Job Scheduling with Apache AirFlow 2.0 in 10 Minutes"),
                    html.P("Workflow Management System made easy — explained with Python examples."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/job-scheduling-with-apache-airflow-2-0-in-10-minutes-16d19f548a46",
    target="_blank",
)

article_heroku = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.CardHeader("Software Engineering"),
                    html.H5("Heroku + Docker in 10 Minutes"),
                    html.P("Deployment for Python applications made easy — and it’s free."),
                ],
            ),
        ],
        className=f"zoom background-{color_se}",
    ),
    href="https://medium.com/towards-data-science/heroku-docker-in-10-minutes-f4329c4fd72f",
    target="_blank",
)


def articles_tab():
    return html.Div(
        [
            content_header("Articles"),
            html.Div([
                article_coursera,
                article_dashboard,
                article_reinforcement_learning,
                article_ensemble,
                article_best_practices,
                article_programming,
                article_sphinx,
                article_bigtree,
                article_logging,
                article_lists,
                article_pytest,
                article_unittest,
                article_fastapi,
                article_multithreading,
                article_mlflow,
                article_airflow,
                article_heroku,
            ],
                className="card-group",
            ),
        ],
    )
