import collections
import pandas as pd

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash import dash_table
from sanstyle.github.file import lfs_url

from app import app
import dash
dash.register_page(__name__)
url = lfs_url('SanstyleLab/plotly-dastsets',
              'gapminderDataFiveYear.csv')
df = pd.read_csv(url)
countries = set(df['country'])


layout = html.Div([
    dcc.Store(id='memory-output'),
    dcc.Dropdown(id='memory-countries', options=[
        {'value': x, 'label': x} for x in countries
    ], multi=True, value=['Canada', 'United States']),
    dcc.Dropdown(id='memory-field', options=[
        {'value': 'lifeExp', 'label': 'Life expectancy'},
        {'value': 'gdpPercap', 'label': 'GDP per capita'},
    ], value='lifeExp'),
    html.Div([
        dcc.Graph(id='memory-graph'),
        dash_table.DataTable(
            id='memory-table',
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])
])


@app.callback(Output('memory-output', 'data'),
              Input('memory-countries', 'value'))
def filter_countries(countries_selected):
    if not countries_selected:
        # 返回初始加载/没有选定国家时的所有行。
        return df.to_dict('records')
    filtered = df.query('country in @countries_selected')
    return filtered.to_dict('records')


@app.callback(Output('memory-table', 'data'),
              Input('memory-output', 'data'))
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate
    return data


@app.callback(Output('memory-graph', 'figure'),
              Input('memory-output', 'data'),
              Input('memory-field', 'value'))
def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate
    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    for row in data:
        a = aggregation[row['country']]
        a['name'] = row['country']
        a['mode'] = 'lines+markers'
        a['x'].append(row[field])
        a['y'].append(row['year'])
    return {'data': list(aggregation.values())}
