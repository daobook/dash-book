from dash.dependencies import Input, Output
from dash import html
from datetime import datetime
import time
from app import app
import dash
dash.register_page(__name__)
layout = html.Div(
    [
        html.Button("execute fast callback", id="button_3"),
        html.Button("execute slow callback", id="button_4"),
        html.Div(children="callback not executed", id="first_output_3"),
        html.Div(children="callback not executed", id="second_output_3"),
        html.Div(children="callback not executed", id="third_output_3"),
    ]
)


@app.callback(
    Output("first_output_3", "children"),
    Input("button_3", "n_clicks"))
def first_callback(n):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f'in the fast callback it is {current_time}'


@app.callback(
    Output("second_output_3", "children"), Input("button_4", "n_clicks"))
def second_callback(n):
    time.sleep(5)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f'in the slow callback it is {current_time}'


@app.callback(
    Output("third_output_3", "children"),
    Input("first_output_3", "children"),
    Input("second_output_3", "children"))
def third_callback(n, m):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f'in the third callback it is {current_time}'
