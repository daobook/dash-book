import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import index
from examples.run import callback_example

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname.startswith('/examples/'):
        return callback_example(pathname)
    # else:
    #     return '404'


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=5555, threaded=True)
    # app.run_server(app, debug=True, port=5555, threaded=True)
