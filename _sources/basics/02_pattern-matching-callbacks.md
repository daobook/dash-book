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

# 模式匹配回调

参考：[Pattern-Matching Callbacks | Dash for Python Documentation | Plotly](https://dash.plotly.com/pattern-matching-callbacks)

Dash 1.11.0 的新功能！（需要 `dash-renderer` 1.4.0或更高版本）

模式匹配的回调选择器 `MATCH`，`ALL` 和 `ALLSMALLER` 允许您编写响应或更新任意数量或动态数量的组件的回调。

## ALL 的简单例子

此示例呈现任意数量的 `dcc.Dropdown` 元素，并且只要任何 `dcc.Dropdown` 元素发生更改，就会触发回调。尝试添加一些下拉菜单并选择其值，以查看应用程序如何更新。

```python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

layout = html.Div([
    html.Button("Add Filter", id="add-filter", n_clicks=0),
    html.Div(id='dropdown-container', children=[]),
    html.Div(id='dropdown-container-output')
])


@app.callback(
    Output('dropdown-container', 'children'),
    Input('add-filter', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):
    new_dropdown = dcc.Dropdown(
        id={
            'type': 'filter-dropdown',
            'index': n_clicks
        },
        options=[{'label': i, 'value': i}
                 for i in ['NYC', 'MTL', 'LA', 'TOKYO']]
    )
    children.append(new_dropdown)
    return children


@app.callback(
    Output('dropdown-container-output', 'children'),
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
)
def display_output(values):
    return html.Div([
        html.Div('Dropdown {} = {}'.format(i + 1, value))
        for (i, value) in enumerate(values)
    ])
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/all-pattern',
      className='w3-pale-blue',
      height=300)
```

有关此示例的一些注意事项：

- 注意`dcc.Dropdown`中的`id`是字典而不是字符串。这是我们为模式匹配回调启用的一项新功能（以前，ID 必须为字符串）。
- 在第二个回调中，我们有`Input({'type': 'filter-dropdown', 'index': ALL}, 'value')`。这意味着“匹配具有ID字典的任何输入，其中`'type'`是`'filter-dropdown'`并且`'index'`是任何东西。只要任何下拉列表的`value`属性发生变化，就将其所有值发送到回调中。”
- ID 字典的键和值（`type`, `index`, `filter-dropdown`）是任意的。可以将其命名为`{'foo': 'bar', 'baz': n_clicks}`。
- 但是，出于可读性考虑，我们建议使用 `type`, `index` 或 `id` 之类的键。`type`可以用来引用类或集合的动态组件，而`index`或`id`可以用来引用在该集合内匹配的组件。在此示例中，我们只有一组动态组件，但是在更复杂的应用程序中或者在使用`MATCH`时，您可能具有多组动态组件（请参见下文）。
- 实际上，在此示例中，我们实际上并不需要`'type': 'filter-dropdown'`。相同的回调将与`Input({'index': ALL}, 'value')`一起使用。如果您创建了多组动态组件，我们将`'type': 'filter-dropdown'`作为额外的说明符。
- 组件属性本身（例如，`value`）无法通过模式进行匹配，只有 ID 是动态的。
- 此示例使用带有`State`的通用模式-单击按钮时，`dropdown-container`组件中当前显示的下拉列表集将传递到回调中。在回调中，新的下拉列表将添加到列表中，然后返回。
- 您还可以使用`dash.callback_context`来访问输入和状态，并知道哪个输入已更改。这是在页面上呈现两个下拉菜单时数据可能看起来的样子。
    - `dash.callback_context.triggered`。请注意，`prop_id`是没有空格的字符串化字典。

    ```python
    [
        {
            'prop_id': '{"index":0,"type":"filter-dropdown"}.value',
            'value': 'NYC'
        }
    ]
    ```
    - `dash.callback_context.inputs`。请注意，键是没有空格的字符串化字典。

    ```python
    {
        '{"index":0,"type":"filter-dropdown"}.value': 'NYC',
        '{"index":1,"type":"filter-dropdown"}.value': 'LA'
    }
    ```

    - `dash.callback_context.inputs_list`。列表中的每个元素都对应于一个输入声明。如果输入声明之一与模式匹配，则它将包含值列表。

    ```python
    [
        [
            {
                'id': {
                    'index': 0,
                    'type': 'filter-dropdown'
                },
                'property': 'value',
                'value': 'NYC'
            },
            {
                'id': {
                    'index': 1,
                    'type': 'filter-dropdown'
                },
                'property': 'value',
                'value': 'LA'
            }
        ]
    ]
    ```

    - `dash.callback_context.outputs_list`

    ```python
        {
    'id': 'dropdown-container-output',
    'property': 'children'
    }
    ```

## MATCH 的简单示例

像`ALL`一样，当组件的任何属性更改时，`MATCH`都会触发回调。但是，`MATCH`不会将所有值都传递给回调函数，而只会将单个值传递给回调函数。与其更新单个输出，不如更新与之`"matched"`的动态输出。

```python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH

layout = html.Div([
    html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
    html.Div(id='dynamic-dropdown-container', children=[]),
])


@app.callback(
    Output('dynamic-dropdown-container', 'children'),
    Input('dynamic-add-filter', 'n_clicks'),
    State('dynamic-dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):
    new_element = html.Div([
        dcc.Dropdown(
            id={
                'type': 'dynamic-dropdown',
                'index': n_clicks
            },
            options=[{'label': i, 'value': i}
                     for i in ['NYC', 'MTL', 'LA', 'TOKYO']]
        ),
        html.Div(
            id={
                'type': 'dynamic-output',
                'index': n_clicks
            }
        )
    ])
    children.append(new_element)
    return children


@app.callback(
    Output({'type': 'dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value'),
    State({'type': 'dynamic-dropdown', 'index': MATCH}, 'id'),
)
def display_output(value, id):
    return html.Div('Dropdown {} = {}'.format(id['index'], value))
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/match-pattern',
      className='w3-pale-blue',
      height=300)
```

关于此示例的注释：

- `display_dropdowns`回调返回具有相同`index`的两个元素：dropdown 和 div。
- 第二个回调使用`MATCH`选择器。使用此选择器，我们要求 Dash 执行以下操作：
    1. 每当 id 为`'type': 'dynamic-dropdown'`的任何组件的`value`属性更改时，都会触发回调：`Input({'type': 'dynamic-dropdown', 'index': MATCH}, 'value')`
    2. 使用id `'type': 'dynamic-output'` 和与输入的相同索引匹配的`index`更新组件：`Output({'type': 'dynamic-output', 'index': MATCH}, 'children')`
    3. 将下拉列表的 `id` 传递到回调中：`State({'type': 'dynamic-dropdown', 'index': MATCH}, 'id')`
- 使用`MATCH`选择器，对于每个`Input`或`State`，仅将一个值传递到回调中。这与之前的`ALL`选择器示例不同，在该示例中，Dash 将所有值都传递到了回调中。
- 请注意，设计将输入与输出`"line up"`的 ID 字典非常重要。`MATCH`约定是 Dash 将更新具有与`id`相同的动态ID的任何输出。在这种情况下，“动态ID”是索引的值，我们设计了布局以返回具有相同索引值的下拉列表和div。
- 在某些情况下，了解哪个动态组件已更改可能很重要。如上所述，您可以通过在回调中将`id`设置为`State`来访问它。
- 您还可以使用`dash.callback_context`来访问输入和状态，并知道哪个输入已更改。`output_list`在`MATCH`中特别有用，因为它可以告诉您该特定的回调调用负责更新哪个动态组件。这是我们更改第一个下拉菜单后在页面上呈现两个下拉菜单时数据的外观。
    - `dash.callback_context.triggered`。请注意，`prop_id`是没有空格的字符串化字典。

    ```python
    [
        {
            'prop_id': '{"index":0,"type":"dynamic-dropdown"}.value',
            'value': 'NYC'
        }
    ]
    ```
    - `dash.callback_context.inputs`。请注意，键是没有空格的字符串化字典。
    ```python
    {
        '{"index":0,"type":"dynamic-dropdown"}.value': 'NYC'
    }
    ```
    - `dash.callback_context.inputs_list`。列表中的每个元素都对应于一个输入声明。如果输入声明之一与模式匹配，则它将包含值列表。
    ```python
    [
        [
            {
                'id': {
                    'index': 0,
                    'type': 'dynamic-dropdown'
                },
                'property': 'value',
                'value': 'NYC'
            }
        ]
    ]
    ```
    - `dash.callback_context.outputs_list`
    ```python
    {
        'id': {
            'index': 0,
            'type': dynamic-output'
        },
        'property': 'children'
    }
    ```

## ALLSMALLER 的简单示例

在下面的示例中，`ALLSMALLER`用于传递页面上所有索引小于与 div 对应的索引的下拉列表的值。

下例中的用户界面显示了过滤器结果，随着我们应用每个其他下拉菜单，过滤器结果在每个过滤器中都越来越具体。

`ALLSMALLER`仅可用于输入和状态项，并且必须用于在输出项中具有`MATCH`的键上。

`ALLSMALLER`并非总是必要的（您通常可以使用ALL并在回调中过滤掉索引），但是它将使您的逻辑更简单。

```python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER
import pandas as pd

from sanstyle.github.file import lfs_url

url = lfs_url('SanstyleLab/plotly-dastsets',
              'gapminder2007.csv')
df = pd.read_csv(url)
layout = html.Div([
    html.Button('Add Filter', id='add-filter-ex3', n_clicks=0),
    html.Div(id='container-ex3', children=[]),
])


@app.callback(
    Output('container-ex3', 'children'),
    Input('add-filter-ex3', 'n_clicks'),
    State('container-ex3', 'children'))
def display_dropdowns(n_clicks, existing_children):
    existing_children.append(html.Div([
        dcc.Dropdown(
            id={
                'type': 'filter-dropdown-ex3',
                'index': n_clicks
            },
            options=[{'label': i, 'value': i} for i in df['country'].unique()],
            value=df['country'].unique()[n_clicks]
        ),
        html.Div(id={
            'type': 'output-ex3',
            'index': n_clicks
        })
    ]))
    return existing_children


@app.callback(
    Output({'type': 'output-ex3', 'index': MATCH}, 'children'),
    Input({'type': 'filter-dropdown-ex3', 'index': MATCH}, 'value'),
    Input({'type': 'filter-dropdown-ex3', 'index': ALLSMALLER}, 'value'),
)
def display_output(matching_value, previous_values):
    previous_values_in_reversed_order = previous_values[::-1]
    all_values = [matching_value] + previous_values_in_reversed_order

    dff = df[df['country'].str.contains('|'.join(all_values))]
    avgLifeExp = dff['lifeExp'].mean()

    # Return a slightly different string depending on number of values
    if len(all_values) == 1:
        return html.Div('{:.2f} is the life expectancy of {}'.format(
            avgLifeExp, matching_value
        ))
    elif len(all_values) == 2:
        return html.Div('{:.2f} is the average life expectancy of {}'.format(
            avgLifeExp, ' and '.join(all_values)
        ))
    else:
        return html.Div('{:.2f} is the average life expectancy of {}, and {}'.format(
            avgLifeExp, ', '.join(all_values[:-1]), all_values[-1]
        ))
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/allsmaller-pattern',
      className='w3-pale-blue',
      height=300)
```

- 在上面的示例中，尝试添加一些过滤器，然后更改第一个下拉列表。请注意，更改此下拉菜单将如何更新具有依赖于该下拉菜单的索引的每个`html.Div`的文本。
- 也就是说，只要索引小于它的任何下拉列表发生变化，每个`html.Div`都会被更新。
- 因此，如果添加了10个过滤器，并且第一个下拉列表已更改，则Dash将触发您的回调10次，一次更新每个`html.Div`，这取决于已更改的`dcc.Dropdown`。
- 如上所述，您还可以使用`dash.callback_context`来访问输入和状态，并知道哪个输入已更改。这是在更改第一个下拉列表后，使用页面上呈现的两个下拉列表更新第二个div时数据的外观。
    - `dash.callback_context.triggered`。请注意，prop_id是没有空格的字符串化字典。
    ```python
    [
        {
            'prop_id': '{"index":0,"type":"filter-dropdown-ex3"}.value',
            'value': 'Canada'
        }
    ]
    ```
    - `dash.callback_context.inputs`。请注意，键是没有空格的字符串化字典。
    ```python
    {
        '{"index":1,"type":"filter-dropdown-ex3"}.value': 'Albania',
        '{"index":0,"type":"filter-dropdown-ex3"}.value': 'Canada'
    }
    ```
    - `dash.callback_context.inputs_list`。列表中的每个元素都对应于一个输入声明。如果输入声明之一与模式匹配，则它将包含值列表。

    ```python
    [
        {
            'id': {
                'index': 1,
                'type': 'filter-dropdown-ex3'
            },
            'property': 'value',
            'value': 'Albania'
        },
        [
            {
                'id': {
                    'index': 0,
                    'type': 'filter-dropdown-ex3'
                },
                'property': 'value',
                'value': 'Canada'
            }
        ]
    ]
    ```
    - `dash.callback_context.outputs_list`

    ```python
    {
        'id': {
            'index': 1,
            'type': output-ex3'
        },
        'property': 'children'
    }
    ```

## Todo App

创建 Todo 应用程序是一个经典的 UI 练习，它演示了常见的“创建，读取，更新和删除”（CRUD）应用程序中的许多功能。

```python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import callback_context

layout = html.Div([
    html.Div('Dash To-Do list'),
    dcc.Input(id="new-item"),
    html.Button("Add", id="add"),
    html.Button("Clear Done", id="clear-done"),
    html.Div(id="list-container"),
    html.Div(id="totals")
])

style_todo = {"display": "inline", "margin": "10px"}
style_done = {"textDecoration": "line-through", "color": "#888"}
style_done.update(style_todo)


@app.callback(
    [
        Output("list-container", "children"),
        Output("new-item", "value")
    ],
    [
        Input("add", "n_clicks"),
        Input("new-item", "n_submit"),
        Input("clear-done", "n_clicks")
    ],
    [
        State("new-item", "value"),
        State({"index": ALL}, "children"),
        State({"index": ALL, "type": "done"}, "value")
    ]
)
def edit_list(add, add2, clear, new_item, items, items_done):
    triggered = [t["prop_id"] for t in callback_context.triggered]
    adding = len([1 for i in triggered if i in (
        "add.n_clicks", "new-item.n_submit")])
    clearing = len([1 for i in triggered if i == "clear-done.n_clicks"])
    new_spec = [
        (text, done) for text, done in zip(items, items_done)
        if not (clearing and done)
    ]
    if adding:
        new_spec.append((new_item, []))
    new_list = [
        html.Div([
            dcc.Checklist(
                id={"index": i, "type": "done"},
                options=[{"label": "", "value": "done"}],
                value=done,
                style={"display": "inline"},
                labelStyle={"display": "inline"}
            ),
            html.Div(text, id={"index": i},
                     style=style_done if done else style_todo)
        ], style={"clear": "both"})
        for i, (text, done) in enumerate(new_spec)
    ]
    return [new_list, "" if adding else new_item]


@app.callback(
    Output({"index": MATCH}, "style"),
    Input({"index": MATCH, "type": "done"}, "value")
)
def mark_done(done):
    return style_done if done else style_todo


@app.callback(
    Output("totals", "children"),
    Input({"index": ALL, "type": "done"}, "value")
)
def show_totals(done):
    count_all = len(done)
    count_done = len([d for d in done if d])
    result = "{} of {} items completed".format(count_done, count_all)
    if count_all:
        result += " - {}%".format(int(100 * count_done / count_all))
    return result
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/todo',
      className='w3-pale-blue',
      height=300)
```