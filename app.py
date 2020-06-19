import dash
import os
import sys

from flask import Flask

from callbacks import register_callbacks
from layouts import main_layout
from routes import register_routes

module_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, module_path)
os.chdir(module_path)

server = Flask(__name__, static_url_path='/', static_folder='docs/build/html/')
app = dash.Dash(__name__, server=server)
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
