from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
import dash
dash.register_page(__name__)

layout = html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),
    html.Div(id='output-container-range-slider')
])


@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('my-range-slider', 'value')])
def update_output(value):
    return f'你选择了 "{value}"'
