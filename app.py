import dash

from flask import Flask

from callbacks import register_callbacks
from layouts import main_layout
from routes import register_routes

# server = Flask(__name__, static_url_path='/', static_folder='docs/build/html/')
meta_tags = [
    {
        'property': 'og:title',
        'content': 'Tools to make life easier'
    }, {
        'property': 'og:description',
        'content': 'Helper tool that automates repetitive data analysis tasks, and perform predictions and optimizations that are computationally expensive'
    }, {
        'property': 'og:image',
        'content': 'https://svgshare.com/i/MTw.svg'
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
