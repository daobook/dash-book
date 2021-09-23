import pandas as pd
from dash import html

from sanstyle.github.file import lfs_url


url = lfs_url('SanstyleLab/plotly-dastsets',
              'simple/usa-agricultural-exports-2011.csv')
df = pd.read_csv(url)


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


layout = html.Div(children=[
    html.H4(children='美国农业出口 (2011)'),
    generate_table(df)
])
