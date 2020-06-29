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
        'property': 'og:type',
        'content': 'website'
    }, {
        'property': 'og:title',
        'content': 'Tools to make life easier'
    }, {
        'property': 'og:description',
        'content': 'Automate repetitive data analysis tasks and perform predictions and optimizations'
    }, {
        'property': 'og:image',
        'content': 'https://i.ibb.co/KrjyLmg/favicon-google.png'
    }, {
        'property': 'og:image:width',
        'content': '1200'
    }, {
        'property': 'og:image:height',
        'content': '627'
    }, {
        'property': 'twitter:title',
        'content': 'Tools to make life easier'
    }, {
        'property': 'twitter:description',
        'content': 'Automate repetitive data analysis tasks and perform predictions and optimizations'
    }, {
        'property': 'twitter:image',
        'content': 'https://i.ibb.co/cFwJMGg/favicon-twitter.png'
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
