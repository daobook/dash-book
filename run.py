import asyncio
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from layouts import index

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index.layout
    # elif pathname.startswith('/examples/'):
    #     return callback_example(pathname)
    # else:
    #     return '404'

app.config.suppress_callback_exceptions = True  # 用于支持多页应用

if __name__ == '__main__':
    import asyncio
    from dash_xinet.server import run_server

    port = 8057
    # app.run_server(debug=True, port=5555, threaded=True)
    # app.run_server(app, debug=True, port=5555, threaded=True)
    run = run_server(app, layout,
                     port=port, debug=True
                     )
    asyncio.run(run)
else:
    app.layout = layout
    server = app.server  # 用于 Dash 服务器部署
