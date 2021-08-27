import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app


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
