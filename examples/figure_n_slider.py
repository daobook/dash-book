import pandas as pd

from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from sanstyle.github.file import lfs_url

from app import app
import dash
dash.register_page(__name__)
url = lfs_url('SanstyleLab/plotly-dastsets',
              'gapminderDataFiveYear.csv')

df = pd.read_csv(url)


layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)
    fig.update_layout(transition_duration=500)
    return fig
