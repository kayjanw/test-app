import warnings

import dash
import gevent.monkey

gevent.monkey.patch_all()

from callbacks.articles import register_callbacks_articles
from callbacks.callbacks import register_callbacks
from callbacks.change_calculator import (
    register_callbacks as register_callbacks_change_calculator,
)
from callbacks.chat import register_callbacks as register_callbacks_chat
from callbacks.event_planner import (
    register_callbacks as register_callbacks_event_planner,
)
from callbacks.mbti import register_callbacks as register_callbacks_mbti
from callbacks.rng import register_callbacks as register_callbacks_rng
from callbacks.trade import register_callbacks as register_callbacks_trade
from callbacks.trip_planner import register_callbacks as register_callbacks_trip_planner
from callbacks.wnrs import register_callbacks as register_callbacks_wnrs
from layouts.main import main_layout
from routes import register_routes

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


meta_tags = [
    {"name": "author", "content": "Kay Jan WONG"},
    {
        "name": "description",
        "content": "Kay Jan's Side Project - "
        "Automate repetitive data analysis tasks, perform predictions and optimizations, and play games",
    },
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    {"property": "og:type", "content": "website"},
    {"property": "og:title", "content": "Tools to make life fun and easier"},
    {
        "property": "og:description",
        "content": "Automate repetitive data analysis tasks, "
        "perform predictions and optimizations, and play games",
    },
    {"property": "og:image", "content": "https://i.ibb.co/KrjyLmg/favicon-google.png"},
    {"property": "og:image:width", "content": "1200"},
    {"property": "og:image:height", "content": "627"},
    {"property": "twitter:title", "content": "Tools to make life easier and fun"},
    {
        "property": "twitter:description",
        "content": "Automate repetitive data analysis tasks, "
        "perform predictions and optimizations, and play games",
    },
    {
        "property": "twitter:image",
        "content": "https://i.ibb.co/cFwJMGg/favicon-twitter.png",
    },
    {"http-equiv": "Cache-control", "content": "public"},
    {
        "name": "google-site-verification",
        "content": "3AcDEhXtFa35ByGGTh-Fy8bDeDY6hUQUqYcrfh0mGso",
    },
]
app = dash.Dash(__name__, title="bowwow", update_title=None, meta_tags=meta_tags)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.layout = main_layout()

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-178463864-1"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-178463864-1');
    </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

print_function = False
register_callbacks_articles(app, print_function)
register_callbacks(app, print_function)
register_callbacks_change_calculator(app, print_function)
register_callbacks_chat(app, print_function)
register_callbacks_event_planner(app, print_function)
register_callbacks_mbti(app, print_function)
register_callbacks_rng(app, print_function)
register_callbacks_trade(app, print_function)
register_callbacks_trip_planner(app, print_function)
register_callbacks_wnrs(app, print_function)
register_routes(app)


if __name__ == "__main__":
    app.run_server(debug=True)
