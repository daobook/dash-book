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

(dash:advanced-callbacks)=
# 高级回调

参考：[Advanced Callbacks](https://dash.plotly.com/advanced-callbacks)

## 使用 `PreventUpdate` 捕获错误

在某些情况下，您不想更新回调输出。您可以通过在回调函数中引发 `PreventUpdate` 异常来实现此目的。

```{include} ../examples/prevent_update.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/prevent-update',
      className='w3-pale-blue',
      height=70)
```

## 使用 `dash.no_update` 显示错误

此示例说明如何使用 `dash.no_update` 来部分更新输出，从而在保留先前输入的同时显示错误。

```{include} ../examples/no_update.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/no-update',
      className='w3-pale-blue',
      height=160)
```

## 确定使用 `dash.callback_context` 触发了哪个输入

除了 `n_clicks` 之类的事件属性会在事件发生（在这种情况下为单击）时发生更改之外，还有一个全局变量 `dash.callback_context`，仅在回调内部可用。它具有以下特性：

- `triggered`：已更改属性的列表。在初始加载时，此属性将为空，除非 `Input` 属性从另一个初始回调获得值。在用户操作之后，它是一个长度为 1 的列表，除非单个组件的两个属性同时更新，例如值和时间戳或事件计数器。
- `inputs` 和 `states`：允许您通过 `id` 和 `prop` 而不是通过函数 `args` 来访问回调参数。这些具有字典的形式 `{'component_id.prop_name': value}`

这是如何完成此操作的示例：

```{include} ../examples/callback_context.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/callback-context',
      className='w3-pale-blue',
      height=470)
```

```{hint}
在 v0.38.0 之前的版本中，您需要比较诸如 `n_clicks_timestamp` 之类的时间戳属性以查找最近的点击。虽然 `*_timestamp` 的现有用法现在仍可以继续工作，但是不建议使用此方法，并且可以在以后的更新中将其删除。一个例外是 `dcc.Store` 的 `Modifyed_timestamp`，它可以安全使用，并且不建议使用。
```

(dash:advanced-callbacks/memoization)=
## 通过 memoization 提高性能

借助 Memoization，可以存储函数调用的结果来绕开长时间的计算。

为了更好地理解记忆的工作原理，让我们从一个简单的示例开始。

```python
import time
import functools


@functools.lru_cache(maxsize=32)
def slow_function(inputs):
    time.sleep(10)
    return f'Input was {inputs}'
```

第一次调用 `slow_function('test')` 将需要 10 秒钟。第二次使用相同的参数调用它几乎不需要花费时间，因为先前计算的结果已保存在内存中并可以重复使用。

Dash 文档的 [](dash:performance) 部分深入研究了利用多个进程和线程以及 memoization 来进一步提高性能的情况。

## 何时执行回调？

本节介绍了 `dash-renderer` 前端客户端可以向 Dash 后端服务器（或客户端回调代码）发出请求以执行回调函数的情况。

### 首次加载 Dash 应用程序时

首次加载应用程序时，Dash 应用程序中的所有回调均以其输入的初始值执行。这称为回调的“初始调用”。若要了解如何抑制此行为，请参阅 Dash 回调的 [`prevent_initial_call`](dash:prevent-callbacks-from-being-executed-on-initial-load) 属性的文档。

重要的是要注意，当 Dash 应用程序最初由 `dash-renderer` 前端客户端加载到 Web 浏览器中时，将递归检查其整个回调链。

这使得 `dash-renderer` 可以预测执行回调的顺序，因为当回调的输入是尚未触发的其他回调的输出时，它们将被阻塞。为了取消阻止执行这些回调，必须先执行其输入立即可用的回调。此过程通过确保仅在所有回调的输入都达到其最终值时才请求执行回调，来帮助 `dash-renderer` 最大程度地减少其使用的时间和精力，并避免不必要地重画页面。

检查以下 Dash 应用程序：

```{include} ../examples/first_load.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/first-load',
      className='w3-pale-blue',
      height=100)
```

请注意，当完成该应用程序的 Web 浏览器加载并准备好与用户进行交互时，`html.Div` 组件不会像在应用程序的 `layout` 中声明的那样说“未执行回调”，而是 `n_clicks` 为 `None`，这是由于 `change_text()` 回调正在执行。这是因为回调的“初始调用”是使用值为 `None` 的 `n_clicks` 发生的。

### 用户交互的直接结果

通常，回调是用户交互的直接结果，例如单击按钮或在下拉菜单中选择一项。当发生这种交互时，Dash 组件将其新值传递给 `dash-renderer` 前端客户端，该客户端再请求 Dash 服务器执行将新更改的值作为输入的任何回调函数。

如果 Dash 应用程序具有多个回调，则 `dash-renderer` 会根据是否可以使用新更改的输入立即执行回调来请求执行回调。如果多个输入同时更改，则将请求全部执行它们。

这些请求是以同步还是异步方式执行取决于 Dash 后端服务器的特定设置。如果它在多线程环境中运行，那么所有回调都可以同时执行，并且它们将根据执行速度返回值。但是，在单线程环境中，回调将按照服务器接收到的顺序一次执行一次。

在上面的示例应用程序中，单击按钮将导致执行回调。

### 用户交互的间接结果

当用户与组件进行交互时，生成的回调可能会有输出，这些输出本身就是其他回调的输入。`dash-renderer`将阻止此类回调的执行，直到执行了其输出为其输入的回调为止。

请使用以下 Dash 应用程序：

```{include} ../examples/indirect_result.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/indirect-result',
      className='w3-pale-blue',
      height=110)
```

上面的 Dash 应用演示了回调如何链接在一起。请注意，如果您先单击 `"execute slow callback"`，然后单击 `"execute fast callback"`，则直到慢速回调完成执行后，才会执行第三个回调。这是因为第三个回调将第二个回调的输出作为其输入，这使 `dash-renderer` 知道应将其执行延迟到第二个回调完成之后。

### 将 Dash 组件添加到 `layout` 时

回调可能会将新的 Dash 组件插入 Dash 应用程序的 `layout`中。如果这些新组件本身是其他回调函数的输入，则它们在 Dash 应用程序 `layout` 中的出现将触发这些回调函数被执行。

在这种情况下，可能会发出多个请求以执行相同的回调函数。如果已经请求了有问题的回调，并且在将新组件（也就是其输入）添加到 `layout` 之前返回了其输出，则会发生这种情况。

(dash:prevent-callbacks-from-being-executed-on-initial-load)=
### 阻止在初始组件渲染时执行回调

您可以使用 `prevent_initial_call` 属性来阻止在其输入最初出现在 Dash 应用程序的 `layout` 中时触发回调。

此属性在最初加载 Dash 应用程序的 `layout` 时适用，并且在触发回调时将新组件引入到 `layout` 中时也适用。

```{include} ../examples/prevent_initial_call.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/prevent-initial-call',
      className='w3-pale-blue',
      height=150)
```

但是，仅当应用程序初始加载时在应用程序 `layout` 中同时存在回调输出和输入的情况下，以上行为才适用。

重要的是要注意，在应用程序最初加载之后，如果回调的输入由于另一个回调的结果而被插入到 `layout` 中，除非输出与该输入一起插入，否则 `prevent_initial_call` 不会阻止回调的触发！

换句话说，如果在将回调的输入插入到 `layout` 之前，该回调的输出已经存在于应用程序`layout`中，那么当将输入首次插入到`layout`中时，`prevent_initial_call` 将不会阻止其执行。

考虑以下示例：

```python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import urllib
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='layout-div'),
    html.Div(id='content')
])


@app.callback(Output('content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    return html.Div([
        dcc.Input(id='input', value='hello world'),
        html.Div(id='output')
    ])


@app.callback(Output('output', 'children'),
              Input('input', 'value'),
              prevent_initial_call=True)
def update_output(value):
    print('>>> update_output')
    return value


@app.callback(Output('layout-div', 'children'),
              Input('input', 'value'),
              prevent_initial_call=True)
def update_layout_div(value):
    print('>>> update_layout_div')
    return value
```

在这种情况下，`prevent_initial_call`将防止由于`display_page()`回调而将其输入首次插入应用程序 `layout` 时触发 `update_output()` 回调。这是因为执行回调时，回调的输入和输出都已包含在应用 `layout` 中。

但是，由于应用程序 `layout` 仅包含回调的输出，而不包含其输入，因此 `prevent_initial_call` 不会阻止 `update_layout_div()` 回调触发。由于此处指定了 `prevent_callback_exceptions = True`，因此 Dash 必须假定在初始化应用程序时输入出现在应用程序 `layout` 中。从本示例中的输出元素的角度来看，新输入组件的处理方式就像已为现有输入提供了新值一样，而不是将其视为初始呈现。

## 循环回调

从 dash v1.19.0 开始，您可以在同一回调中创建循环更新。

不支持涉及多个回调的循环回调链。

循环回调可用于保持多个输入彼此同步。

## 将 Slider 与 Text Input 同步的示例

```{include} ../examples/sync_slider_text.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/sync-slider-text',
      className='w3-pale-blue',
      height=110)
```

## 显示两个具有不同单位的输入示例

```{include} ../examples/convert_temperature.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/convert-temperature',
      className='w3-pale-blue',
      height=110)
```

## 同步两个清单

```{include} ../examples/sync_checklists.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/sync-checklists',
      className='w3-pale-blue',
      height=80)
```