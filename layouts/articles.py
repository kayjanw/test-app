import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from layouts.main import content_header

topic_colour_dict = {
    "Productivity": "lightblue",
    "Dashboard": "blue",
    "Data Science": "red",
    "Coding Best Practices": "green",
    "Software Engineering": "yellow",
}


card_list = [
    (
        "Productivity",
        "5 Tips After Completing 100 Coursera Courses",
        "Reflections on my e-learning journey.",
        "https://towardsdatascience.com/5-tips-after-completing-100-coursera-courses-1ee5a35e72a4?sk=bd67c6888a7a552c8f5fbdedf64f7554",
    ),
    (
        "Dashboard",
        "Advancing to Professional Dashboard with Python, using Dash",
        "Advanced ways to enhance initial skeleton code.",
        "https://towardsdatascience.com/advancing-to-professional-dashboard-with-python-using-dash-and-plotly-1e8e5aa4c668?sk=e021c653a51b578a8382828f68ce483e",
    ),
    (
        "Data Science",
        "6 Reinforcement Learning Algorithms Explained",
        "Introduction to reinforcement learning terminologies, basics, and concepts.",
        "https://towardsdatascience.com/6-reinforcement-learning-algorithms-explained-237a79dbd8e?sk=23d7245dbdaf0c0082edd579c623da8d",
    ),
    (
        "Data Science",
        "CatBoost vs. LightGBM vs. XGBoost",
        "Which is the best algorithm?",
        "https://towardsdatascience.com/catboost-vs-lightgbm-vs-xgboost-c80f40662924?sk=abe57d6a8c3965f6997b04970b6dda0e",
    ),
    (
        "Data Science",
        "7 Evaluation Metrics for Clustering Algorithms",
        "In-depth explanation with Python examples of unsupervised learning evaluation metrics",
        "https://towardsdatascience.com/7-evaluation-metrics-for-clustering-algorithms-bdc537ff54d2?sk=565cf6977935e51f1622e2b28ed8d8cc",
    ),
    (
        "Data Science",
        "Feature Encoding Techniques in Machine Learning with Python Implementation",
        "6 feature encoding techniques to consider for your data science workflows",
        "https://towardsdatascience.com/feature-encoding-techniques-in-machine-learning-with-python-implementation-dbf933e64aa?sk=47d0a64ab3eed9bc3babf59870152aff",
    ),
    (
        "Coding Best Practices",
        "3 Tips for Writing Clean Codes Beyond Coding Best Practices",
        "Write elegant, modular, understandable, and maintainable codes.",
        "https://towardsdatascience.com/3-tips-for-writing-clean-codes-beyond-coding-best-practices-c53b04120c3?sk=f8e1323aeaee830874422abb6ad1dc69",
    ),
    (
        "Coding Best Practices",
        "How to Learn New Programming Languages Easily",
        "Pick up any new programming language — with Python, Java, and Go examples.",
        "https://towardsdatascience.com/how-to-learn-new-programming-languages-easily-1e6e29d3898a?sk=30e945a9e327624a0c710192be0a294d",
    ),
    (
        "Coding Best Practices",
        "Advanced Code Documentation Beyond Comments and Docstrings",
        "Use Sphinx and Read the Docs for a user-friendly interface to understand codebase — even for non-technical users.",
        "https://towardsdatascience.com/advanced-code-documentation-beyond-comments-and-docstrings-2cc5b2ace28a?sk=e27cf3ec7723a1af37271e83e4dff888",
    ),
    (
        "Software Engineering",
        "Python Tree Implementation with BigTree",
        "Integrating trees with Python lists, dictionaries, and pandas DataFrames.",
        "https://medium.com/towards-data-science/python-tree-implementation-with-bigtree-13cdabd77adc",
    ),
    (
        "Software Engineering",
        "Basic to Advanced Logging with Python in 10 Minutes",
        "Logging crash course with common logging issues addressed.",
        "https://towardsdatascience.com/basic-to-advanced-logging-with-python-in-10-minutes-631501339650?sk=a17d61aeff13d6791168042330fbc3b1",
    ),
    (
        "Software Engineering",
        "3 Data Structures for Faster Python Lists",
        "Choose your lists wisely.",
        "https://towardsdatascience.com/3-data-structures-for-faster-python-lists-f29a7e9c2f92?sk=85d35153dca175f49f9fe63cc1f7bb35",
    ),
    (
        "Software Engineering",
        "Pytest with Marking, Mocking, and Fixtures in 10 Minutes",
        "Write robust unit tests with Python pytest.",
        "https://towardsdatascience.com/pytest-with-marking-mocking-and-fixtures-in-10-minutes-678d7ccd2f70?sk=9707ed3994d15e2e2a0344f4dfec425b",
    ),
    (
        "Software Engineering",
        "Unit Testing with Mocking in 10 Minutes",
        "Test your codebase effectively with the built-in unittest Python package.",
        "https://towardsdatascience.com/unit-testing-with-mocking-in-10-minutes-e28feb7e530?sk=4a2f6e8cb1a99d626e70977a45d68b6f",
    ),
    (
        "Software Engineering",
        "Implementing FastAPI in 10 Minutes",
        "Develop, test, and use your custom API.",
        "https://towardsdatascience.com/implementing-fastapi-in-10-minutes-d161cdd7c075?sk=d2bac1f4257bcfb7eeadf06a27224ce6",
    ),
    (
        "Software Engineering",
        "Multithreading and Multiprocessing in 10 Minutes",
        "Multitasking made easy with Python examples.",
        "https://towardsdatascience.com/multithreading-and-multiprocessing-in-10-minutes-20d9b3c6a867?sk=1710068be298b1687b9f96e40b39b81c",
    ),
    (
        "Software Engineering",
        "Experiment Tracking with MLflow in 10 Minutes",
        "Managing Machine Learning Lifecycle made easy — explained with Python examples.",
        "https://towardsdatascience.com/experiment-tracking-with-mlflow-in-10-minutes-f7c2128b8f2c?sk=6ee34637af9dacd734dbc57ac4213209",
    ),
    (
        "Software Engineering",
        "Job Scheduling with Apache AirFlow 2.0 in 10 Minutes",
        "Workflow Management System made easy — explained with Python examples.",
        "https://towardsdatascience.com/job-scheduling-with-apache-airflow-2-0-in-10-minutes-16d19f548a46?sk=df2921ed50a7ddded0360cf248162092",
    ),
    (
        "Software Engineering",
        "Google Cloud vs. Fly.io as Heroku Alternatives",
        "Comparison of free-tier Docker deployments",
        "https://towardsdatascience.com/google-cloud-vs-fly-io-as-heroku-alternatives-1f5a47716a58?sk=c9d1395f5833b63e5e6af795748bf58d",
    ),
    (
        "Software Engineering",
        "Heroku + Docker in 10 Minutes",
        "Deployment for Python applications made easy — and it’s free.",
        "https://towardsdatascience.com/heroku-docker-in-10-minutes-f4329c4fd72f?sk=568b7e38903f7175080faa8e7cbe42ee",
    ),
]

button_dict = {
    "variant": "filled",
    "size": "xs",
    "compact": True,
    "radius": "lg",
    "style": {"margin": "0px 10px 10px 0px"},
}


def articles_tab():
    card_div_list = []
    for idx, values in enumerate(card_list):
        topic, title, description, link = values
        card_div_list.append(
            html.A(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.CardHeader(topic),
                                html.H5(title),
                                html.P(description),
                            ],
                        ),
                    ],
                    className=f"zoom background-{topic_colour_dict[topic]}",
                ),
                id={"type": "card-article", "id": f"article-{topic}", "idx": idx},
                href=link,
                target="_blank",
            )
        )
    button_div_list = []
    for topic, colour in topic_colour_dict.items():
        button_div_list.append(
            dmc.Button(
                topic,
                id={"type": "button-article", "id": f"article-{topic}"},
                className=f"background-{colour}",
                **button_dict,
            )
        )

    return html.Div(
        [
            content_header(
                "Articles",
                [
                    DashIconify(icon="openmoji:rainbow", height=40),
                    "Friend Links for my Towards Data Science articles",
                ],
            ),
            html.Div(button_div_list),
            html.Div(card_div_list, className="card-group"),
        ],
    )
