from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from app import app
import dash
dash.register_page(__name__)

layout = html.Div([
    html.Button('点击这里查看内容', id='show-secret'),
    html.Div(id='body-div')
])


@app.callback(
    Output(component_id='body-div', component_property='children'),
    Input(component_id='show-secret', component_property='n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "大象是唯一不会跳的动物"
