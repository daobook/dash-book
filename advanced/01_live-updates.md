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

(dash:live-updates)=
# 实时更新

参考：[Live Updates | Dash for Python Documentation | Plotly](https://dash.plotly.com/live-updates)

## `dcc.Interval`

Dash 中的组件通常通过用户交互进行更新，比如：选择下拉菜单，拖动滑块，悬停在点上。

如果您正在构建用于监视的应用程序，您可能希望每隔几秒或几分钟更新应用程序中的组件。[`dash_core_components.Interval`](dash:dcc/location) 元素允许您按预定义的时间间隔更新组件。`n_interval` 属性是一个整数，每经过 `interval` 毫秒时间间隔就自动增加一次。你可以在你的应用程序的 `callback` 中监听这个变量，以按预先定义的时间间隔触发回调。

此示例从实时卫星反馈中提取数据，并每秒钟更新图表和文本。

```{include} ../examples/live_update.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]

from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/live-update',
      className='w3-pale-blue',
      height=523)
```

## 页面加载更新

默认情况下，Dash 应用程序将 `app.layout` 存储在内存中。这确保当应用程序启动时，布局只计算一次。

如果你将 `app.layout` 设置为一个函数，那么你就可以在每次页面加载时提供动态布局。

例如，如果你的 `app.layout` 是这样的：

```python
import datetime

import dash
import dash_html_components as html

app.layout = html.H1('The time is: ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    app.run_server(debug=True)
```

然后你的应用程序将显示应用程序启动的时间。

如果您将此更改为一个函数，那么每次刷新页面都会计算一个新的 `datetime`。试一试：

```python
import datetime

import dash
import dash_html_components as html
from jupyter_dash import JupyterDash as Dash

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
```

```{attention}
你需要写 `app.layout = serve_layout`，而不是 `app.layout = serve_layout()`。也就是说，将 `app.layout` 定义为实际的函数实例。
```

您可以将其与 [](dash:performance) 结合起来，每小时或每天提供一个独特的 `layout`，并在此期间从内存提供计算出 `layout`。