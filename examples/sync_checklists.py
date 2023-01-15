from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash import callback_context
from app import app
import dash
dash.register_page(__name__)
options = [
    {"label": "New York City", "value": "NYC"},
    {"label": "Montréal", "value": "MTL"},
    {"label": "San Francisco", "value": "SF"},
]
all_cities = [option["value"] for option in options]

layout = html.Div(
    [
        dcc.Checklist(
            id="all-checklist",
            options=[{"label": "All", "value": "All"}],
            value=[],
            labelStyle={"display": "inline-block"},
        ),
        dcc.Checklist(
            id="city-checklist",
            options=options,
            value=[],
            labelStyle={"display": "inline-block"},
        ),
    ]
)


@app.callback(
    Output("city-checklist", "value"),
    Output("all-checklist", "value"),
    Input("city-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(cities_selected, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "city-checklist":
        all_selected = ["All"] if set(
            cities_selected) == set(all_cities) else []
    else:
        cities_selected = all_cities if all_selected else []
    return cities_selected, all_selected
