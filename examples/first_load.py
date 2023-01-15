from dash.dependencies import Input, Output
from dash import html
from app import app
import dash
dash.register_page(__name__)
layout = html.Div(
    [
        html.Button("执行回调", id="button_1"),
        html.Div(children="回调不执行", id="first_output_1"),
        html.Div(children="回调不执行", id="second_output_1"),
    ]
)


@app.callback(
    Output("first_output_1", "children"),
    Output("second_output_1", "children"),
    Input("button_1", "n_clicks")
)
def change_text(n_clicks):
    return [f'n_clicks 是 {str(n_clicks)}', f'n_clicks is {str(n_clicks)}']
