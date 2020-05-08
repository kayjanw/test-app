import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
	html.Div([
		html.H1('Title of banner')
		],
		className='banner'),
	html.Div(),
	html.Div()
	])


if __name__ == '__main__':
	app.run_server(debug=True)
