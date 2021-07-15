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

(dash:external-resources)=
# 添加 CSS 和 JS 以覆盖页面加载模板

参考：[Adding CSS & JS and Overriding the Page-Load Template | Dash for Python Documentation | Plotly](https://dash.plotly.com/external-resources)

Dash 应用程序通过 CSS 和 JavaScript 在 web 浏览器中呈现。在页面加载时，Dash 提供一个小的 HTML 模板，其中包括渲染应用程序所需的 CSS 和 JavaScript 引用。这一章涵盖了你需要知道的关于配置这个 HTML 文件以及关于在 Dash 应用程序中包括外部 CSS 和 JavaScript 的一切。

## 添加自定义 CSS 和 JavaScript

在你的 Dash 应用程序中包含自定义 CSS 或 JavaScript 是很简单的。你只需在 `app` 目录的根目录下创建一个名为 `assets` 的文件夹，并在该文件夹中包含你的 CSS 和 JavaScript 文件。Dash 会自动提供这个文件夹中包含的所有文件。默认情况下，请求资产的 `url` 是 `/assets`，但是你可以用 `assets_url_path` 参数将其自定义为 `dash.Dash`。

```{div} w3-yellow
建议：你需要在 Dash 构造函数中包含 `__name__`。
```

也就是说，`app = dash.Dash(__name__)` 而不是 `app = dash.Dash()`。理由见 [dash-app-does-not-load-assets-and-app-index-string](https://community.plotly.com/t/dash-app-does-not-load-assets-and-app-index-string/12178/10?u=chriddyp)。

## 示例：包含本地 CSS 和 JavaScript

我们将创建几个文件：`app.py`，一个名为 `assets` 的文件夹，以及该文件夹中的三个文件：

```sh
- app.py
- assets/
    |-- typography.css
    |-- header.css
    |-- custom-script.js
```

````{tabbed} app
```python
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H5('Overview'),
            html.Div('''
                This is an example of a simple Dash app with
                local, customized CSS.
            ''')
        ])
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```
````

````{tabbed} custom-script
```javascript
alert('如果您看到此警告，说明您的自定义 JavaScript 脚本已经运行！')
```
````

````{tabbed} typography
```{include} ../assets/typography.css
:code: css
```
````

````{tabbed} header
```{include} ../assets/header.css
:code: css
```
````

当你运行 `app.py` 时，你的应用看起来应该是这样的：

```{code-cell} ipython3
:tags: [remove-input]
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/external-resources',
      className='w3-pale-blue',
      height=150)
```

在自动添加 `assets` 时，你需要牢记以下几点:

1. 以下文件类型将自动包括:
    - CSS 文件后缀为 `.css`
    - 以 `.js` 作为后缀的 JavaScript 文件
    - 一个名为 `favicon.ico` 的文件(页面标签的图标)
2. Dash 将包括文件在字母数字顺序的文件名。因此，如果你需要确保文件名的顺序(例如 `10_typography.css`, `20_header.css`)，我们建议你在文件名前加上数字前缀。
3. 你可以使用正则过滤器 `app = dash.Dash(assets_ignore='.*ignored.*')` 来忽略 `assets` 文件夹中的某些文件。这将阻止 Dash 加载包含上述模式的文件。
4. 如果你想包含来自远程 URL 的CSS，请参阅下一节。
5. 你的自定义 CSS 将包含在 Dash 组件 CSS 之后。
6. 建议在 dash init 中添加`__name__`，以确保加载 `assets` 文件夹中的资源，例如：`app = dash.Dash(__name__, meta_tags=[...])`。当您通过其他命令行运行应用程序时(如 `flask` 命令或 `gunicorn/waitress`)，`__main__` 模块将不再位于 `app.py` 所在的位置。通过明确设置 `__name__`， `Dash` 将能够正确地找到相对 `assets` 文件夹。

## 添加外部 CSS / JavaScript

你可以通过 `external_stylesheets` 和 `external_scripts` init 关键字将托管在你的 Dash 应用程序上的资源添加到外部。

资源可以是字符串，也可以是包含标签属性（`src`、`integrity`、`crossorigin` 等）的字典。你可以两者混合。

外部 css/js 文件在 `assets` 之前被加载。

例如：

```python
import dash
import dash_html_components as html


# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)
```

## 自定义 Dash 的文件或浏览器标签标题

文档标题是出现在网页浏览器选项卡中的网页名称。

默认值是 `Dash`。

在 Dash 1.14.0 中，你可以使用 `title=` 关键字来定制这个标题:

```python
app = dash.Dash(__name__, title='Weekly Analytics')
```

## 根据 URL 或选项卡动态更新文档标题

要动态设置文档标题，可以使用`clientside callback` 作为一个副作用更新 `document.title`。下面的示例设置 `document.title`的基础上，当前选择的选项卡。

```python
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='blank-output'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
])


app.clientside_callback(
    """
    function(tab_value) {
        if (tab_value === 'tab-1') {
            document.title = 'Tab 1'
        } else if (tab_value === 'tab-2') {
            document.title = 'Tab 2'
        }
    }
    """,
    Output('blank-output', 'children'),
    Input('tabs-example', 'value')
)

if __name__ == '__main__':
    app.run_server(debug=True)
```

基于 URL 更新页面将是类似的：回调的输入将是 `dcc.Location` 的 `pathname` 属性。关于 `dcc.Location`，请参阅 [url 和多页应用程序](https://dash.plotly.com/urls)章节。

## 定制或删除 Dash 的`"Updating..."`消息

当一个回调运行时，Dash 更新文档标题(出现在你的浏览器标签)与`"Updating..."`消息。

使用 `update_title=属性` 定制此消息：

```python
app = dash.Dash(__name__, update_title='Loading...')
```

或者，通过设置`update_title=None`来阻止此消息的出现：

```python
app = dash.Dash(__name__, update_title=None)
```

## 自定义 Dash 的 HTML index 模板

Dash 的 UI 是通过 Dash 的 `React.js` 前端动态生成的。因此，在页面加载时，Dash提 供一个非常小的 HTML 模板字符串，其中包括渲染页面所需的 CSS 和 JavaScript 以及一些简单的 HTML 元标记。

这个简单的 HTML 字符串是可定制的。如果你想自定义这个字符串:

- 定制页面中包含 CSS 或 JavaScript 的方式。例如，如果您想包含远程脚本，或者如果您想在 Dash 组件 CSS 之前包含 CSS
- 在你的应用程序中包含自定义元标记。注意，元标记也可以通过 `meta_tags` 参数添加(下面的例子)。
- 通过自己实例化 `DashRenderer` 类，包含一个自定义版本的`dash-renderer`。你可以通过下面的例子提供一个`hooks`配置对象来添加请求钩子。

### Option 1 - index_string

添加一个`index_string`来修改默认的 HTML 索引模板：

```python
import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div>My Custom header</div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>My Custom footer</div>
    </body>
</html>
'''

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
```

`{%key%}`是模板变量，Dash 会用默认属性自动填充。可用的`key`是：

- `{%metas%}` (optional)：注册的`meta`标签包含在`dash.Dash`中的`meta_tags`参数中。
- `{%favicon%}` (optional)：如果在`assets`文件夹中找到`favicon`链接标签。
- `{%css%}` (optional)：&lt;link&gt; CSS 资源的标签。这些资源包括 Dash 组件库CSS资源以及在`assets`文件夹中找到的任何 CSS 资源。
- `{%title%}` (optional)：页面内容 &lt;title&gt;标签。了解更多关于[&lt;title/&gt;](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title)
- `{%config%}` (required)：一个自动生成的标签，包括从 Dash 的后端到前端的配置设置(`dash-renderer`)。
- `{%app_entry%}` (required)：渲染 Dash 布局的容器。
- `{%scripts%}` (required)：渲染 Dash 应用所需的 JavaScript 脚本集。这包括 Dash 组件的 JavaScript 文件以及在 `assets` 文件夹中找到的任何 JavaScript 文件。
- `{%renderer%}` (required)：通过调用`new DashRenderer()`实例化`dash-renderer`的`JavaScript`脚本

### Option 2 - interpolate_index

如果你的 HTML 内容不是静态的，或者你想 introspect 或修改模板变量，那么你可以覆盖 `Dash.interpolate_index` 方法。

```python
import dash
import dash_html_components as html


class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):
        # Inspect the arguments by printing them
        print(kwargs)
        return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>My App</title>
            </head>
            <body>

                <div id="custom-header">My custom header</div>
                {app_entry}
                {config}
                {scripts}
                {renderer}
                <div id="custom-footer">My custom footer</div>
            </body>
        </html>
        '''.format(
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'])

app = CustomDash()

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
```

不像`index_string`方法，我们使用模板字符串变量，传递到`interpolate_index`的关键字变量已经被求值了。

在上面的例子中，当我们打印`interpolate_index`的输入参数时，应该会看到这样的输出：

```python
{
    'title': 'Dash',
    'app_entry': '\n<div id="react-entry-point">\n    <div class="_dash-loading">\n        Loading...\n    </div>\n</div>\n',
    'favicon': '',
    'metas': '<meta charset="UTF-8"/>',
    'scripts': '<script src="https://unpkg.com/react@15.4.2/dist/react.min.js"></script>\n<script src="https://unpkg.com/react-dom@15.4.2/dist/react-dom.min.js"></script>\n<script src="https://unpkg.com/dash-html-components@0.14.0/dash_html_components/bundle.js"></script>\n<script src="https://unpkg.com/dash-renderer@0.20.0/dash_renderer/bundle.js"></script>',
    'renderer': '<script id="_dash-renderer" type="application/javascript">var renderer = new DashRenderer();</script>',
    'config': '<script id="_dash-config" type="application/json">{"requests_pathname_prefix": "/", "url_base_pathname": "/"}</script>',
    'css': ''
}
```

`scripts`和`css`键的值可能会不同，这取决于您包含的组件库或`assets`文件夹中的文件。

### 使用请求钩子定制 dash-renderer

为了实例化你自己的`dash-renderer`版本，你可以覆盖 Dash 的HTML Index Template，并提供你自己的脚本来代替标准脚本。这个脚本应该在某处调用`var renderer = new DashRenderer();`，它实例化了`DashRenderer`类。当你设置`app.index_string`时，你可以将这个脚本添加到你的 index HTML 中，或者你可以像这样简单地覆盖`app.renderer`：

```python
import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.renderer = 'var renderer = new DashRenderer();'

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
```

当你提供你自己的`DashRenderer`时，你也可以传入一个钩子对象来保存`request_pre`和`request_post`函数。这些请求钩子将在`Dash`向其后端发出请求之前和之后被触发。这里有一个例子：

```python
import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.renderer = '''
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log(payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log(payload);
        console.log(response);
    }
})
'''

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
```

请注意，`request_pre`函数将正在发送的请求的有效负载作为其参数，而`request_post`函数将有效负载和服务器的响应同时作为参数。这些可以在我们的功能中改变，允许你修改`Dash`发送给服务器的响应和请求对象。在上面的例子中，`request_pre`函数在每次服务器调用之前被触发，在这个例子中，它将`console.log()`请求参数。`request_post`函数将在每次服务器调用后触发，在我们的示例中还将打印出响应参数。

## 定制 Meta 标记

要在你的应用程序中添加自定义元标签，你可以覆盖`Dash`的 HTML 索引模板。另外，`Dash` 提供了一个快捷方式：你可以直接在 `Dash` 构造函数中指定 `meta` 标签：

```python
import dash
import dash_html_components as html

app = dash.Dash(meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'My description'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }
])

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)
```