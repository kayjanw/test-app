***************************************
Creating Dash Application
***************************************

Installing Dash
------------------------

Dash package is distributed on PyPI and can be installed with pip

::

    pip install dash

This should also install other dash packages such as ``dash-core-components`` and ``dash-html-components``


Make your first Dash app
------------------------
Create a python file named ``app.py`` and get started!

Dash has underlying Flask app that is available by calling ``app.server``

.. code:: python

    import dash

    app = dash.Dash(__name__)
    server = app.server

Alternatively, Flask app instance can be passed into Dash.
This implementation makes it easier to use Flask endpoints.

.. code:: python

    import dash
    from flask import Flask

    server = Flask(__name__)
    app = dash.Dash(__name__, server=server)

There are some other app configurations that are recommended to have.
Layout can be rendered with ``dash_core_components`` and ``dash_html_components`` components.

.. code:: python

    import dash_core_components as dcc
    import dash_html_components as html

    app.config.suppress_callback_exceptions = True  # suppresses initial callback error
    app.css.config.serve_locally = True             # reads in CSS from local files (optional, defaults to True anyway)
    app.scripts.config.serve_locally = True         # reads in scripts from local files (optional, defaults to True anyway)
    app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                id='page-content',
                children=['Hello World!'])
        ])                                          # your page content!

Every action on the web application, i.e. button click or dropdown selection can trigger a callback action.
Remember to give the widget item an ``id`` so that the callback knows which item to refer to!
One example of a callback can be as follows

.. code:: python

    from dash.dependencies import Input, Output
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return html.Div([f"This is page: {pathname}"])

Finally, write the line of code that will execute the application!
Users may set ``debug=False`` in production environment.

.. code:: python

    if __name__ == '__main__':
        app.run_server(debug=True)

The full list of web widgets such as dropdowns, checklists, sliders etc. and more usage examples can be found on
dash_ documentation website

.. _dash: https://dash.plotly.com/
