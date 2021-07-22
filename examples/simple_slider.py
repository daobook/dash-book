import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app


layout = html.Div([
    dcc.Slider(
        id='my-slider',
        min=0,
        max=20,
        step=0.5,
        value=10,
    ),
    html.Div(id='slider-output-container')
])


@app.callback(
    Output('slider-output-container', 'children'),
    [Input('my-slider', 'value')])
def update_output(value):
    return f'你选择了 "{value}"'
