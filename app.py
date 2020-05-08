import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = html.Div([

	# Left banner
	html.Div([
	    html.Div(
	        html.H1([
	        	'KJ Wong'
	        ],
	            style={
	               	'font-family': 'Kalam',
	               	'color': 'white'
	            }
	        ),
	        style={
	        	'margin-top': '15vh',
	        	'margin-left': '10px',
	        }
	    ),
	    html.Div(
	    	dcc.Tabs(
	    		id='tabs-parent',
	    		value='tab-1',
	    		vertical=True,
	    		parent_className='custom-tabs',
                children=[
                     dcc.Tab(label='About Me', value='tab-1', className='custom-tab'),
                     dcc.Tab(label='Keyboard (WIP)', value='tab-2', className='custom-tab'),
                     dcc.Tab(label='Other fun stuff (WIP)', value='tab-3', className='custom-tab'),
                ],
                colors={
                	'background': '#89CFF0'
                },
                style={
                	'width': '100%'
                }
            )
        )],
		style={
			'display': 'inline-block',
			'width': '22vw',
			'height': '97vh',
			'background-color': '#89CFF0',
		}),

	# Right contents
	html.Div([
			'main body'
		],
			id='tab-content',
			style={
				'width': '76vw',
				'height': '97vh',
				'float': 'right',
				'margin-left': '1px',
				'border': '1px solid black'
			})
	])


if __name__ == '__main__':
	app.run_server(debug=True)
