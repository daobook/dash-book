# 在回调之间共享数据

参考：[Part 5\. Sharing Data Between Callbacks | Dash for Python Documentation | Plotly](https://dash.plotly.com/sharing-data-between-callbacks)

[Dash 回调入门指南](dash:interactive) 中解释的 Dash 核心原则之一是：**Dash 回调 绝不能修改超出其作用域的变量**。修改任何**全局**变量是不安全的。本章说明了原因，并提供了一些用于在回调之间共享状态的替代模式。

## 为什么要共享状态？

在某些应用中，您可能会有多个回调，这些回调依赖于昂贵的数据处理任务，例如进行 SQL 查询，运行模拟或下载数据。

您可以让一个回调运行该任务，然后将结果共享给其余的回调，而不是让每个回调都运行相同的昂贵任务。

现在，您可以为一个回调提供 [多个输出](dash:multiple-outputs)，这种需求已得到一定程度的缓解。这样，该昂贵的任务可以一次完成，并立即在所有输出中使用。但是在某些情况下，这还是不理想的，例如，如果有简单的后续任务可以修改结果，例如单位转换。我们只需要将结果从华氏温度更改为摄氏温度，就不必重复大型数据库查询！

## Dash 是无状态的

Dash 被设计成一个无状态框架。

无状态框架具有更强的可伸缩性和健壮性。您访问的大多数网站都是在无状态服务器上构建的。

它们具有更强的可伸缩性，因为向应用程序添加更多计算能力很简单。要扩展应用程序以服务更多用户或运行更多计算，只需在单独的进程中运行应用程序的更多“副本”。在生产中，这可以通过 `gunicorn` 的 worker 命令来完成：

```sh
gunicorn app:server --workers 8
```

或者在多个 Docker 容器或服务器上运行应用程序，并在它们之间实现负载平衡。

无状态框架更加健壮，因为一个进程可能失败，而其他进程可以继续为请求提供服务。在 Dash Enterprise Kubernetes 中，这些容器可以运行在单独的服务器上，甚至是单独的区域，提供针对服务器故障的弹性。

使用无状态框架，用户会话不会与服务器进程一一对应。每个回调请求都可以在任何可用的进程上执行。`gunicorn` 将检查哪个进程不忙于运行回调，并将新的回调请求发送给该进程。这意味着一些进程可以平衡 10 个或 100 个并发用户的请求，只要这些请求不是在同一时间发生（它们通常不会！）。

## 为什么 `global` 变量会破坏您的应用程序

Dash 旨在在多用户环境中工作，在该环境中，多个人可以同时查看该应用程序，并且将进行**独立的会话**。

如果您的应用程序使用修改后的 `global` 变量，则一个用户的会话可以将变量设置为一个值，这将影响下一个用户的会话。

Dash 还设计为能够与 **多个 python worker** 一起运行，以便可以并行执行回调。这通常是使用类似的语法在 `gunicorn` 上完成的：

```shell
$ gunicorn --workers 4 app:server
```

（`app`指的是名为 `app.py` 的文件，而 `server` 指的是该文件中名为 `server` 的变量：`server = app.server`）。

当 Dash 应用程序跨多个工作程序运行时，它们的内存不会共享。这意味着，如果您在一个回调中修改全局变量，则该修改将不会应用于其余的工作程序。

<details><summary>这是一个带有回调的应用程序的草图，该回调会在其作用域之外修改数据。由于上述原因，这种类型的模式<em>无法可靠地运行</em>。</summary>

```python
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 1, 4],
    'c': ['x', 'y', 'z'],
})

layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['c'].unique()],
        value='a'
    ),
    html.Div(id='output'),
])


@app.callback(Output('output', 'children'),
              Input('dropdown', 'value'))
def update_output_1(value):
    # 这里，'df '是一个“在这个函数范围之外”的变量的例子。
    # 在回调函数中修改或重新赋值这个变量是不安全的。
    global df
    df = df[df['c'] == value]  # do not do this, this is not safe!
    return len(df)
```
</details>

<details><summary>要解决此示例，只需将过滤器重新分配给回调中的新变量，或遵循本指南下一部分概述的策略之一。</summary>

```python
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 1, 4],
    'c': ['x', 'y', 'z'],
})

layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['c'].unique()],
        value='a'
    ),
    html.Div(id='output'),
])


@app.callback(Output('output', 'children'),
              Input('dropdown', 'value'))
def update_output_1(value):
    # 安全地将筛选器重新分配给一个新变量
    filtered_df = df[df['c'] == value]
    return len(filtered_df)
```
</details>

## 回调之间共享数据

为了在多个 Python 进程之间安全地共享数据，我们需要将数据存储在每个进程可访问的位置。

有三个主要位置可存储此数据：

1. 借助 [](dash:dcc/store) 在用户的浏览器会话中存储

2. 在磁盘上（例如在文件或新数据库上）

3. 服务器端内存跨进程和服务器共享，比如 Redis 数据库。

下面的三个示例说明了这些方法。

## 示例1 使用 `dcc.Store` 在浏览器中存储数据

```{note}
注意：这个例子是用“hidden div”来实现的。我们推荐使用 `dcc.Store` 代替。将数据存储在浏览器客户端的内存中，而不是浏览器的 DOM 中，这样的意图就更清楚了。
```

要在用户浏览器的会话中保存数据，请执行以下操作：

- 通过使用 <https://community.plotly.com/t/sharing-a-dataframe-between-plots/6173> 中解释的方法将数据保存为 Dash 前端存储的一部分来实现
- 数据必须转换为 JSON 或者 base64 编码的二进制数据才能存储和传输
- 以这种方式缓存的数据将仅在用户的当前会话中可用。
    - 如果您打开新的浏览器，则应用程序的回调将始终计算数据。数据仅在会话内的回调之间进行缓存和传输。
    - 因此，与缓存不同，此方法不会增加应用程序的内存占用。
    - 网络传输可能会产生成本。如果您在回调之间共享 10MB 数据，则该数据将在每个回调之间通过网络传输。
    - 如果网络成本太高，请预先计算聚合并进行传输。您的应用可能不会显示 10MB 的数据，而只会显示其子集或聚合。


````{dropdown} 此示例概述了如何在一个回调中执行昂贵的数据处理步骤，将输出序列化为 JSON 并将其提供为其他回调的输入。本示例使用标准的 Dash 回调并将 JSON 格式的数据存储在应用程序中的隐藏 div 中。
```python
global_df = pd.read_csv('...')
app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),
    # dcc.Store inside the app that stores the intermediate value
    dcc.Store(id='intermediate-value')
])


@app.callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
def clean_data(value):
    # some expensive clean data step
    cleaned_df = your_expensive_clean_or_compute_step(value)

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return cleaned_df.to_json(date_format='iso', orient='split')


@app.callback(Output('graph', 'figure'), Input('intermediate-value', 'data'))
def update_graph(jsonified_cleaned_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure


@app.callback(Output('table', 'children'), Input('intermediate-value', 'data'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table
```
````

## 示例2 前期聚合计算

如果数据很大，则通过网络发送计算的数据可能会很昂贵。在某些情况下，序列化此数据和 JSON 可能也很昂贵。

在许多情况下，您的应用只会显示计算或过滤后的数据的子集或汇总。在这些情况下，您可以在数据处理回调中预先计算聚合，然后将这些聚合传输到其余的回调中。

````{dropdown} 这是一个简单的示例，说明如何将经过筛选或聚合的数据传输到多个回调。

```python
@app.callback(
    Output('intermediate-value', 'data'),
    Input('dropdown', 'value'))
def clean_data(value):
    # an expensive query step
    cleaned_df = your_expensive_clean_or_compute_step(value)

    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    df_1 = cleaned_df[cleaned_df['fruit'] == 'apples']
    df_2 = cleaned_df[cleaned_df['fruit'] == 'oranges']
    df_3 = cleaned_df[cleaned_df['fruit'] == 'figs']

    datasets = {
        'df_1': df_1.to_json(orient='split', date_format='iso'),
        'df_2': df_2.to_json(orient='split', date_format='iso'),
        'df_3': df_3.to_json(orient='split', date_format='iso'),
    }

    return json.dumps(datasets)


@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data'))
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_1'], orient='split')
    figure = create_figure_1(dff)
    return figure


@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data'))
def update_graph_2(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_2'], orient='split')
    figure = create_figure_2(dff)
    return figure


@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data'))
def update_graph_3(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_3'], orient='split')
    figure = create_figure_3(dff)
    return figure
```
````

## 示例3 缓存和信号

这个例子：

- 通过 Flask-Cache 使用 Redis 来存储“全局变量”。该数据通过一个函数访问，该函数的输出由其输入参数缓存并键入键。
- 完成昂贵的计算后，使用隐藏的 div 解决方案将信号发送到其他回调。
- 请注意，除了 Redis 之外，您还可以将其保存到文件系统中。有关更多详细信息，请参见 <https://flask-caching.readthedocs.io/en/latest/>。
- 这种“signaling”很酷，因为它允许昂贵的计算仅占用一个进程。没有这种类型的信令（signaling），每个回调可能最终并行计算昂贵的计算，从而锁定四个进程而不是一个。

该方法的优点还在于，将来的会话可以使用预先计算的值。这对于输入量较少的应用程序将非常有效。

这是此示例的样子。注意事项：

- 我使用`time.sleep(5)`模拟了一个昂贵的过程。
- 应用加载后，需要五秒钟的时间来渲染所有四个图形。
- 初始计算仅阻止一个过程。
- 计算完成后，将发送信号并并行执行四个回调以渲染图形。这些回调中的每一个都从“全局存储”：Redis 或文件系统缓存中检索数据。
- 我在`app.run_server`中设置了`processs = 6`，以便可以并行执行多个回调。在生产中，这可以通过`$ gunicorn --workers 6 --threads 2 app:server`来完成。
- 如果过去已经选择过，则在下拉列表中选择一个值将花费不到五秒钟的时间。这是因为该值是从缓存中提取的。
- 同样，重新加载页面或在新窗口中打开应用程序也很快，因为已经计算了初始状态和初始昂贵的计算量。

![](https://dash.plotly.com/assets/images/gallery/caching.gif)

<details><summary>这是此示例在代码中的样子：</summary>

```python
import os
import copy
import time
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

N = 100

df = pd.DataFrame({
    'category': (
        (['apples'] * 5 * N) +
        (['oranges'] * 10 * N) +
        (['figs'] * 20 * N) +
        (['pineapples'] * 15 * N)
    )
})
df['x'] = np.random.randn(len(df['category']))
df['y'] = np.random.randn(len(df['category']))

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['category'].unique()],
        value='apples'
    ),
    html.Div([
        html.Div(dcc.Graph(id='graph-1'), className="six columns"),
        html.Div(dcc.Graph(id='graph-2'), className="six columns"),
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(id='graph-3'), className="six columns"),
        html.Div(dcc.Graph(id='graph-4'), className="six columns"),
    ], className="row"),

    # hidden signal value
    html.Div(id='signal', style={'display': 'none'})
])


# perform expensive computations in this "global store"
# these computations are cached in a globally available
# redis memory store which is available across processes
# and for all time.
@cache.memoize()
def global_store(value):
    # simulate expensive query
    print('Computing value with {}'.format(value))
    time.sleep(5)
    return df[df['category'] == value]


def generate_figure(value, figure):
    fig = copy.deepcopy(figure)
    filtered_dataframe = global_store(value)
    fig['data'][0]['x'] = filtered_dataframe['x']
    fig['data'][0]['y'] = filtered_dataframe['y']
    fig['layout'] = {'margin': {'l': 20, 'r': 10, 'b': 20, 't': 10}}
    return fig


@app.callback(Output('signal', 'children'), Input('dropdown', 'value'))
def compute_value(value):
    # compute value and send a signal when done
    global_store(value)
    return value


@app.callback(Output('graph-1', 'figure'), Input('signal', 'children'))
def update_graph_1(value):
    # generate_figure gets data from `global_store`.
    # the data in `global_store` has already been computed
    # by the `compute_value` callback and the result is stored
    # in the global redis cached
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'markers',
            'marker': {
                'opacity': 0.5,
                'size': 14,
                'line': {'border': 'thin darkgrey solid'}
            }
        }]
    })


@app.callback(Output('graph-2', 'figure'), Input('signal', 'children'))
def update_graph_2(value):
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'lines',
            'line': {'shape': 'spline', 'width': 0.5},
        }]
    })


@app.callback(Output('graph-3', 'figure'), Input('signal', 'children'))
def update_graph_3(value):
    return generate_figure(value, {
        'data': [{
            'type': 'histogram2d',
        }]
    })


@app.callback(Output('graph-4', 'figure'), Input('signal', 'children'))
def update_graph_4(value):
    return generate_figure(value, {
        'data': [{
            'type': 'histogram2dcontour',
        }]
    })


if __name__ == '__main__':
    app.run_server(debug=True, processes=6)
```
</details>

## 示例4 服务器上基于用户的会话数据

前面的示例在文件系统上缓存了计算，并且所有用户都可以访问这些计算。

在某些情况下，您想使数据与用户会话隔离：一个用户的派生数据不应更新下一个用户的派生数据。一种实现方法是将数据保存在隐藏的 Div中，如第一个示例所示。

执行此操作的另一种方法是使用会话ID将数据保存在文件系统缓存中，然后使用该会话 ID 引用数据。因为数据保存在服务器上而不是通过网络传输，所以此方法通常比“hidden div”方法更快。

该示例最初是在 [Dash 社区论坛主题](https://community.plotly.com/t/capture-window-tab-closing-event/7375/2?u=chriddyp)中讨论的。

这个例子：

- 使用`flask_caching`文件系统缓存来缓存数据。您还可以保存到内存数据库，例如 Redis。
- 将数据序列化为 JSON。
    - 如果您使用的是 Pandas，请考虑使用 Apache Arrow 进行序列化。[社区话题](https://community.plotly.com/t/fast-way-to-share-data-between-callbacks/8024/2)
- 将会话数据最多保存为预期的并发用户数。这样可以防止缓存中的数据过多。
- 通过将隐藏的随机字符串嵌入到应用程序的布局中并在每次页面加载时提供唯一的布局来创建唯一的会话ID。

>注意：与将数据发送到客户端的所有示例一样，请注意，这些会话不一定是安全的或加密的。这些会话ID可能容易受到会话固定样式攻击。

<details><summary>这是此示例在代码中的样子：</summary>

```python
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
from flask_caching import Cache
import os
import pandas as pd
import time
import uuid

external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})


def get_dataframe(session_id):
    @cache.memoize()
    def query_and_serialize_data(session_id):
        # expensive or user/session-unique data processing step goes here

        # simulate a user/session-unique data processing step by generating
        # data that is dependent on time
        now = datetime.datetime.now()

        # simulate an expensive data processing task by sleeping
        time.sleep(5)

        df = pd.DataFrame({
            'time': [
                str(now - datetime.timedelta(seconds=15)),
                str(now - datetime.timedelta(seconds=10)),
                str(now - datetime.timedelta(seconds=5)),
                str(now)
            ],
            'values': ['a', 'b', 'a', 'c']
        })
        return df.to_json()

    return pd.read_json(query_and_serialize_data(session_id))


def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div([
        html.Div(session_id, id='session-id', style={'display': 'none'}),
        html.Button('Get data', id='get-data-button'),
        html.Div(id='output-1'),
        html.Div(id='output-2')
    ])


app.layout = serve_layout


@app.callback(Output('output-1', 'children'),
              Input('get-data-button', 'n_clicks'),
              Input('session-id', 'children'))
def display_value_1(value, session_id):
    df = get_dataframe(session_id)
    return html.Div([
        'Output 1 - Button has been clicked {} times'.format(value),
        html.Pre(df.to_csv())
    ])


@app.callback(Output('output-2', 'children'),
              Input('get-data-button', 'n_clicks'),
              Input('session-id', 'children'))
def display_value_2(value, session_id):
    df = get_dataframe(session_id)
    return html.Div([
        'Output 2 - Button has been clicked {} times'.format(value),
        html.Pre(df.to_csv())
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
```
</details>

![](https://dash.plotly.com/assets/images/gallery/user-session-caching.gif)

在此示例中，需要注意三件事：

- 检索数据时，数据帧的时间戳不会更新。此数据被缓存为用户会话的一部分。
- 最初检索数据需要五秒钟，但是由于已缓存数据，因此连续的查询是即时的。
- 第二个会话显示的数据与第一个会话不同：在回调之间共享的数据被隔离到各个用户会话。

问题？在 [Dash 社区论坛](https://community.plotly.com/c/dash)上讨论这些示例。
