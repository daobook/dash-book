---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: ai
  language: python
  name: ai
---

(dash:layout)=
# 布局

参考：[Part 2 Layout | Dash for Python Documentation | Plotly](https://dash.plotly.com/layout)

```{describe} 导航
本节将通过一些应用程序带领你了解 Dash 应用程序的基础方面：应用程序**布局**。
```

Dash 为应用程序的所有可视组件提供了 Python 类。

载入一些包：

```{code-cell} ipython3
import pandas as pd
import plotly.express as px
from dash import dcc, html
from jupyter_dash import JupyterDash as Dash
```

## 一个简单例子

创建 Dash 应用：

```{code-cell} ipython3
app = Dash(__name__)
```

创建 plotly 图：

```{code-cell} ipython3
# 假设您有一个 "long-form"  数据帧
# 更多选项请参见 https://plotly.com/python/px-arguments/
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
```

设置 Dash 布局：

```{code-cell} ipython3
app.layout = dcc.Graph(
    id='example-graph',
    figure=fig
)
```

<!-- #region -->
运行 Dash 服务：

```python
if __name__ == '__main__':
    app.run_server(debug=True)
```
<!-- #endregion -->

```{code-cell} ipython3
:tags: [remove-input]

import plotly.graph_objects as go
# 展示 fig
go.FigureWidget(fig)
```

```{admonition} 解析
- `layout` 由诸如 `html.Div` 和 `dcc.Graph` 之类的组件树组成。
- 对于每个 HTML 标签都有一个 `html` 库的组件与之对应。比如 `html.H1(children='Hello Dash')` 组件会在应用程序中生成一个 `<h1> Hello Dash </h1>` HTML 元素。
- 并非所有组件都是纯 HTML。`dcc` 描述了交互式的更高级组件，这些组件是通过 `React.js` 库使用 JavaScript，HTML 和 CSS 生成的。
- 每个组件都完全通过关键字属性来描述。Dash 是声明性的：将主要通过这些属性来描述您的应用程序。`children` 属性是特殊的。按照惯例，它始终是第一个属性，这意味着您可以忽略它：`html.H1(children='Hello Dash')` 与 `html.H1('Hello Dash')` 相同。而且，它可以包含字符串，数字，单个组件或组件列表。
- 应用程序中的字体看起来与此处显示的字体可能略有不同。此应用程序使用自定义 CSS 样式表来修改元素的默认样式。您可以在 [CSS 教程](https://dash.plotly.com/external-resources) 中了解更多信息，但现在您可以使用：

:::python
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
:::

以获得与这些示例相同的外观。
```

```{attention} 
（非 Jupyter 环境）
dash 0.30.0 和 dash-renderer 0.15.0 中的新增功能

Dash 包含“热重载”（"hot-reloading"），默认情况下，当您使用 `app.run_server(debug=True)` 运行应用程序时，此功能已激活。这意味着当您更改代码时，Dash 将自动刷新浏览器。

试试看：在应用程序中更改标题“Hello Dash”或更改 x 或 y 数据。您的应用应随您的更改自动刷新。

> 不喜欢热重载吗？您可以使用 `app.run_server(dev_tools_hot_reload=False)` 将其关闭。在 [Dash Dev Tools](https://dash.plotly.com/devtools) 文档中了解更多信息有疑问吗？请参阅[社区论坛热重载](https://community.plotly.com/t/announcing-hot-reload/14177)讨论。
```

可以更新 plotly 图的主题：

```{code-cell} ipython3
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
```

<!-- #region -->
## `html` 样式

`html` 库包含每个 HTML 标记的组件类以及所有 HTML 参数的关键字参数。使用 `style` 属性可以修改 `html.Div` 和 `html.H1` 等组件的内联样式。比如，`html.H1('Hello Dash', style={'textAlign': 'center', 'color': '#7FDBFF'})` 在 Dash 应用程序中呈现为`<h1 style="text-align: center; color: #7FDBFF">Hello Dash</h1>`。

`html` 和 HTML 属性之间有一些重要的区别：

1. HTML 中的 `style` 属性是用分号分隔的字符串。在 Dash 中，仅提供字典。
2. `style` 字典中的键是驼峰式的。比如，可以是 `textAlign`，而不是 `text-align`。
3. HTML `class` 属性是 Dash 中的 `className`。
4. HTML 标记的子代是通过 `children` 关键字参数指定的。按照惯例，这始终是第一个参数，因此经常被省略。

除此之外，您还可以在 Python 上下文中使用所有可用的 HTML 属性和标记。

## 可重复使用的组件

通过使用 Python 编写标记，可以创建复杂的可重用组件（例如表），而无需切换上下文或语言。

这是一个简单的示例，该示例根据 Pandas 数据框生成“表格”。使用以下代码创建一个名为 {download}`../examples/reusable_components.py` 的文件：


```{include} ../examples/reusable_components.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/reusable-components',
      className='w3-pale-blue',
      height=400)
```

## 可视化组件

`dcc` 库包含一个名为 `Graph` 的组件。`Graph` 使用开源 [plotly.js](https://github.com/plotly/plotly.js) JavaScript 图形库呈现交互式数据可视化。Plotly.js 支持超过 35 种图表类型，并以矢量质量 SVG 和高性能 WebGL 呈现图表。

`dcc.Graph` 组件中的 `Figure` 参数与 Plotly 的开源 Python 图形库 `plotly.py` 使用的图形参数相同。请查看 [plotly.py 文档和画廊](https://plotly.com/python) 以了解更多信息。

这是一个从 Pandas 数据框创建散点图的示例。
<!-- #endregion -->

```{code-cell} ipython3
import pandas as pd

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)
layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])
```

```{code-cell} ipython3
:tags: ["remove-input"]
fig
```

```{div} w3-card-4 w3-pale-blue w3-padding
这些图是交互式的和响应式的。将鼠标悬停在点上以查看其值，单击图例项以切换轨迹，单击并拖动以缩放，按住 Shift 键，然后单击并拖动以平移。
```

## Markdown

虽然 Dash 通过 `html` 库公开 HTML，但是用 HTML 编写副本可能很繁琐。要编写文本块，可以使用 `dcc` 库中的 `Markdown` 组件。使用以下代码创建一个名为 `app.py` 的文件：

```{code-cell} ipython3
markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

layout = html.Div([
    dcc.Markdown(children=markdown_text)
])
```

<article class="w3-card w3-padding">
<h3>Dash and Markdown</h3>

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
</article>

## 核心组件

`dcc` 包含一组更高级别的组件，例如下拉列表，图形，Markdown 块等。

像所有 Dash 组件一样，对它们进行了完全声明式的描述。每个可配置的选项都可以用作组件的关键字参数。

在整个教程中，我们将看到许多这些组件。您可以在 [Dash Core 组件库](https://dash.plotly.com/dash-core-components) 中查看所有可用的组件。

以下是一些可用的组件。

```{include} ../examples/intro.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]

from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/intro',
      className='w3-pale-blue',
      height=270)
```

## 总结

Dash 应用程序的 `layout` 描述了该应用程序的外观。`layout` 是组件的分层树。`html` 库提供了所有 HTML 标记的类，关键字参数描述了 HTML 属性，例如样式，`className` 和 `id`。 `dcc` 库生成更高级别的组件，如控件和图形。

更多内容，请参阅：

- [`dcc` 画廊](https://dash.plotly.com/dash-core-components)
- [`html` 画廊](https://dash.plotly.com/dash-html-components)

Dash 的交互性可转到 [](dash:interactive)。
