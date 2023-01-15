from dash.dependencies import Input, Output
from dash import dcc, html
from dash import callback_context

from app import app
import dash
dash.register_page(__name__)
layout = html.Div(
    [
        dcc.Slider(
            id="slider-circular", min=0, max=20,
            marks={i: str(i) for i in range(21)},
            value=3
        ),
        dcc.Input(
            id="input-circular", type="number", min=0, max=20, value=3
        ),
    ]
)


@app.callback(
    Output("input-circular", "value"),
    Output("slider-circular", "value"),
    Input("input-circular", "value"),
    Input("slider-circular", "value"),
)
def callback(input_value, slider_value):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    value = input_value if trigger_id == "input-circular" else slider_value
    return value, value
