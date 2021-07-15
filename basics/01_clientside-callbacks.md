---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: ai
  language: python
  name: ai
---

(dash:clientside-callbacks)=
# 客户端回调

参考：[Clientside Callbacks | Dash for Python Documentation | Plotly](https://dash.plotly.com/clientside-callbacks)

有时，回调可能会导致相当大的开销，尤其是在以下情况下：

- 接收和/或返回大量数据（传输时间）
- 经常被调用（网络延迟，排队，握手）
- 是回调链的一部分，该回调链需要浏览器和 Dash 之间进行多次往返

当回调的开销成本变得太大并且无法进行其他优化时，可以将回调修改为直接在浏览器中运行，而不是向 Dash 发出请求。

回调的语法几乎完全相同。您可以像在声明回调时一样正常使用`Input`和`Output`，但是还可以将 JavaScript 函数定义为`@app.callback`装饰器的第一个参数。

例如，以下回调：

```python
@app.callback(
    Output('out-component', 'value'),
    Input('in-component1', 'value'),
    Input('in-component2', 'value')
)
def large_params_function(largeValue1, largeValue2):
    largeValueOutput = someTransform(largeValue1, largeValue2)
    return largeValueOutput
```

可以重写为使用 JavaScript，如下所示：

```python
from dash.dependencies import Input, Output

app.clientside_callback(
    """
    function(largeValue1, largeValue2) {
        return someTransform(largeValue1, largeValue2);
    }
    """,
    Output('out-component', 'value'),
    Input('in-component1', 'value'),
    Input('in-component2', 'value')
)
```

您还可以选择在 `assets/` 文件夹中的 `.js` 文件中定义函数。为了获得与上面的代码相同的结果，`.js` 文件的内容如下所示：

```js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        large_params_function: function(largeValue1, largeValue2) {
            return someTransform(largeValue1, largeValue2);
        }
    }
});
```

在 Dash 中，回调现在将写为：

```python
from dash.dependencies import ClientsideFunction, Input, Output

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='large_params_function'
    ),
    Output('out-component', 'value'),
    Input('in-component1', 'value'),
    Input('in-component2', 'value')
)
```

## 一个简单的例子

下面是两个使用客户端回调与`dcc.Store`组件一起更新图形的示例。在这些示例中，我们在后端更新了`dcc.Store`组件。为了创建和显示图形，我们在前端有一个客户端回调，该回调添加了一些有关我们使用`"Graph scale"`下的单选按钮指定的`layout`的其他信息。

```python
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import json
from sanstyle.github.file import lfs_url

url = lfs_url('SanstyleLab/plotly-dastsets',
              'gapminderDataFiveYear.csv')

df = pd.read_csv(url)

available_countries = df['country'].unique()

layout = html.Div([
    dcc.Graph(
        id='clientside-graph'
    ),
    dcc.Store(
        id='clientside-figure-store',
        data=[{
            'x': df[df['country'] == 'Canada']['year'],
            'y': df[df['country'] == 'Canada']['pop']
        }]
    ),
    'Indicator',
    dcc.Dropdown(
        id='clientside-graph-indicator',
        options=[
            {'label': 'Population', 'value': 'pop'},
            {'label': 'Life Expectancy', 'value': 'lifeExp'},
            {'label': 'GDP per Capita', 'value': 'gdpPercap'}
        ],
        value='pop'
    ),
    'Country',
    dcc.Dropdown(
        id='clientside-graph-country',
        options=[
            {'label': country, 'value': country}
            for country in available_countries
        ],
        value='Canada'
    ),
    'Graph scale',
    dcc.RadioItems(
        id='clientside-graph-scale',
        options=[
            {'label': x, 'value': x} for x in ['linear', 'log']
        ],
        value='linear'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of figure storage'),
        dcc.Markdown(
            id='clientside-figure-json'
        )
    ])
])


@app.callback(
    Output('clientside-figure-store', 'data'),
    Input('clientside-graph-indicator', 'value'),
    Input('clientside-graph-country', 'value')
)
def update_store_data(indicator, country):
    dff = df[df['country'] == country]
    return [{
        'x': dff['year'],
        'y': dff[indicator],
        'mode': 'markers'
    }]


app.clientside_callback(
    """
    function(data, scale) {
        return {
            'data': data,
            'layout': {
                 'yaxis': {'type': scale}
             }
        }
    }
    """,
    Output('clientside-graph', 'figure'),
    Input('clientside-figure-store', 'data'),
    Input('clientside-graph-scale', 'value')
)


@app.callback(
    Output('clientside-figure-json', 'children'),
    Input('clientside-figure-store', 'data')
)
def generated_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/clientside-callbacks',
      className='w3-pale-blue',
      height=800)
```

请注意，在此示例中，我们通过从数据框中提取相关数据来手动创建`figure`字典。这就是存储在我们的`dcc.Store`组件中的内容； 展开上面的"Contents of figure storage"，以准确查看用于构建图形的内容。

## 使用 Plotly Express 生成 figure

通过 Plotly Express，您可以创建 `figures` 的单行声明。当使用诸如 `plotly_express.Scatter` 创建 graph 时，您将获得一个字典作为返回值。该字典的形状与 `dcc.Graph` 组件的 `figure` 参数相同。（有关`figure`形状的更多信息，请参见[此处](https://plotly.com/python/creating-and-updating-figures/)。）

我们可以重做上面的示例以使用 Plotly Express。

```python
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

import plotly.express as px
from sanstyle.github.file import lfs_url

url = lfs_url('SanstyleLab/plotly-dastsets',
              'gapminderDataFiveYear.csv')

df = pd.read_csv(url)

available_countries = df['country'].unique()
layout = html.Div([
    dcc.Graph(
        id='clientside-graph-px'
    ),
    dcc.Store(
        id='clientside-figure-store-px'
    ),
    'Indicator',
    dcc.Dropdown(
        id='clientside-graph-indicator-px',
        options=[
            {'label': 'Population', 'value': 'pop'},
            {'label': 'Life Expectancy', 'value': 'lifeExp'},
            {'label': 'GDP per Capita', 'value': 'gdpPercap'}
        ],
        value='pop'
    ),
    'Country',
    dcc.Dropdown(
        id='clientside-graph-country-px',
        options=[
            {'label': country, 'value': country}
            for country in available_countries
        ],
        value='Canada'
    ),
    'Graph scale',
    dcc.RadioItems(
        id='clientside-graph-scale-px',
        options=[
            {'label': x, 'value': x} for x in ['linear', 'log']
        ],
        value='linear'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Contents of figure storage'),
        dcc.Markdown(
            id='clientside-figure-json-px'
        )
    ])
])


@app.callback(
    Output('clientside-figure-store-px', 'data'),
    Input('clientside-graph-indicator-px', 'value'),
    Input('clientside-graph-country-px', 'value')
)
def update_store_data(indicator, country):
    dff = df[df['country'] == country]
    return px.scatter(dff, x='year', y=str(indicator))


app.clientside_callback(
    """
    function(figure, scale) {
        if(figure === undefined) {
            return {'data': [], 'layout': {}};
        }
        const fig = Object.assign({}, figure, {
            'layout': {
                ...figure.layout,
                'yaxis': {
                    ...figure.layout.yaxis, type: scale
                }
             }
        });
        return fig;
    }
    """,
    Output('clientside-graph-px', 'figure'),
    Input('clientside-figure-store-px', 'data'),
    Input('clientside-graph-scale-px', 'value')
)


@app.callback(
    Output('clientside-figure-json-px', 'children'),
    Input('clientside-figure-store-px', 'data')
)
def generated_px_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/clientside-callbacks-px',
      className='w3-pale-blue',
      height=800)
```

同样，您可以展开上方的 "Contents of figure storage" 部分，以查看生成的内容。您可能会注意到，这比前面的示例要广泛得多。特别是已经定义了`layout`。因此，我们不必像以前那样创建`layout`，而是必须对 JavaScript 代码中的现有`layout`进行更改。

注意：有一些限制要牢记：

- 客户端回调在浏览器的主线程上执行，并在执行时阻止渲染和事件处理。
- Dash 当前不支持异步客户端回调，如果返回 `Promise`，它将失败。
- 如果您需要引用服务器上的全局变量，或者需要数据库调用，则无法进行客户端回调。
