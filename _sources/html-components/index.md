---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: ai
  language: python
  name: ai
---

(dash:html-components)=
# Dash HTML 组件

参考：[Dash HTML Components | Dash for Python Documentation | Plotly](https://dash.plotly.com/dash-html-components)。

Dash 是一个 web 应用框架，它围绕 HTML、CSS 和 JavaScript 提供了纯 Python 抽象。不用编写 HTML 或使用 HTML 模板引擎，而是使用 Python 结构和 `dash-html-components` 库组成布局。

源代码见：[plotly/dash-html-components](https://github.com/plotly/dash-html-components)。

对于生产 Dash 应用程序，Dash HTML 组件的样式和布局应该与 Dash 企业 [设计工具包](https://plotly.com/dash/design-kit) 管理。

下面是一个简单的 HTML 结构示例：

```python
import dash_html_components as html

html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('Dash 将 Python 类转换为 HTML'),
        html.P("这个转换是由 Dash 的 JavaScript 前端在幕后完成的")
    ])
])
```

它会在你的 web 应用程序中转换（在幕后）成以下 HTML：

```html
<div>
    <h1>Hello Dash</h1>
    <div>
        <p>Dash 将 Python 类转换为 HTML</p>
        <p>这个转换是由 Dash 的 JavaScript 前端在幕后完成的</p>
    </div>
</div>
```

如果您不熟悉 HTML，也不要担心！只需要一些元素和属性，就可以达到 95% 的效果。Dash 的[核心组件库](https://dash.plotly.com/dash-core-components)也支持 [Markdown](http://commonmark.org/help)。


```{code-cell} ipython3
import dash_core_components as dcc

content = '''#### Dash and Markdown

Dash supports [Markdown](http://commonmark.org/help).

Markdown is a simple way to write and format text.
It includes a syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.'''

md = dcc.Markdown(content)
```

<section class="w3-pale-blue">
<h4> Dash and Markdown </h4>

Dash supports [Markdown](http://commonmark.org/help).

Markdown is a simple way to write and format text.
It includes a syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
</section>

如果您正在使用 HTML 组件，那么您还可以访问 `style`、`class` 和 `id` 等属性。所有这些属性都可以在 Python 类中使用。

HTML 元素和 Dash 类基本相同，但有几个关键的区别：

- `style` 是一个字典
- `style` 字典中的属性是驼峰式大小写
- `class` 被重命名为 `className`
- 以像素为单位的样式属性可以仅作为数字提供，而不需使用 `px` 单位

让我们来看一个例子。

```python
import dash_html_components as html

div = html.Div([
    html.Div('Example Div', style={'color': 'blue', 'fontSize': 14}),
    html.P('Example P', className='my-class', id='my-p-element')
], style={'marginBottom': 50, 'marginTop': 25})
```

Dash 代码将呈现以下 HTML 标记：

```
<div style="margin-bottom: 50px; margin-top: 25px;">
    <div style="color: blue; font-size: 14px">
        Example Div
    </div>
    <p class="my-class", id="my-p-element">
        Example P
    </p>
</div>
```

```{attention}
如果你需要直接渲染一个原始的、未转义的 HTML 字符串，你可以使用由 [dash-dangerously-set-inner-html](https://github.com/plotly/dash-dangerously-set-inner-html) 库提供的 `DangerouslySetInnerHTML` 组件。
```

全部元素参考：

```{tableofcontents}
```