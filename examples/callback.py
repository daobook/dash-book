from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
import dash
dash.register_page(__name__)
layout = html.Div([
    html.H6("更改文本框中的值以查看回调操作！"),
    html.Div(["输入：",
              dcc.Input(id='my-input', value='初始值', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'输出：{input_value}'
