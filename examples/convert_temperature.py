from dash.dependencies import Input, Output
from dash import dcc, html
from dash import callback_context
from app import app
import dash
dash.register_page(__name__)
layout = html.Div([
    html.Div('温度变换'),
    '摄氏度',
    dcc.Input(
        id="celsius",
        value=0.0,
        type="number"
    ),
    ' = 华氏温度',
    dcc.Input(
        id="fahrenheit",
        value=32.0,
        type="number",
    ),
])


@app.callback(
    Output("celsius", "value"),
    Output("fahrenheit", "value"),
    Input("celsius", "value"),
    Input("fahrenheit", "value"),
)
def sync_input(celsius, fahrenheit):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "celsius":
        fahrenheit = None if celsius is None else (float(celsius) * 9/5) + 32
    else:
        celsius = None if fahrenheit is None else (
            float(fahrenheit) - 32) * 5/9
    return celsius, fahrenheit
