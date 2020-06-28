import dash

from flask import Flask

from callbacks import register_callbacks
from layouts import main_layout
from routes import register_routes

# server = Flask(__name__, static_url_path='/', static_folder='docs/build/html/')
meta_tags = [
    {
        'name': 'author',
        'content': 'Kay Jan WONG'
    }, {
        'data-react-helmet': 'true',
        'property': 'og:title',
        'content': 'Tools to make life easier'
    }, {
        'data-react-helmet': 'true',
        'property': 'og:description',
        'content': 'Helper tool that automates repetitive data analysis tasks, and perform predictions and optimizations that are computationally expensive'
    }, {
        'data-react-helmet': 'true',
        'property': 'og:image',
        'content': 'https://i.ibb.co/N6mwPyP/favicon.png'
    }, {
        'data-react-helmet': 'true',
        'property': 'og:image:width',
        'content': '512'
    }, {
        'data-react-helmet': 'true',
        'property': 'og:image:height',
        'content': '512'
    },     {
        'data-react-helmet': 'true',
        'property': 'twitter:title',
        'content': 'Tools to make life easier'
    }, {
        'data-react-helmet': 'true',
        'property': 'twitter:description',
        'content': 'Helper tool that automates repetitive data analysis tasks, and perform predictions and optimizations that are computationally expensive'
    }, {
        'data-react-helmet': 'true',
        'property': 'twitter:image',
        'content': 'https://i.ibb.co/N6mwPyP/favicon.png'
    }
]
app = dash.Dash(__name__, meta_tags=meta_tags)
server = app.server
app.title = 'wow'
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.layout = main_layout()

print_function = False
register_callbacks(app, print_function)
register_routes(app)


if __name__ == '__main__':
    app.run_server(debug=True)
