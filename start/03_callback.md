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

(dash:interactive)=
# 回调与交互

参考：[Basic Callbacks | Dash for Python Documentation | Plotly](https://dash.plotly.com/basic-callbacks)

在 [布局](dash:layout) 中，我们了解到 `app.layout` 描述应用程序的外观，并且是组件的分层树。`html` 库提供了所有 HTML 标记的类，关键字参数描述了 HTML 属性，例如 `style`，`className` 和 `id`。`dcc` 库生成更高级别的组件，如控件和图形。本章介绍如何使用回调函数制作 Dash 应用程序：每当输入组件的属性发生更改时 Dash 会自动调用的 Python 函数。

为了获得最佳的用户交互和图表加载性能，生产 Dash 应用程序应考虑 Dash Enterprise 的 [Job Queue](https://plotly.com/dash/job-queue)，[HPC](https://plotly.com/dash/big-data-for-python)，[Datashader](https://plotly.com/dash/big-data-for-python) 和 [horizontal scaling](https://plotly.com/dash/kubernetes) 功能。

让我们从一个交互式 Dash 应用程序的简单示例开始。

为了保证全书的 Dash 应用代码的主题一致，创建文件 {download}`../app.py`，其他应用均需要使用 `from app import app` 载入 `app`。

## 简单的交互

```{include} ../examples/callback.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/callback',
      className='w3-pale-blue',
      height=150)
```

让我们拆解这个例子：

- 我们将应用程序接口的 `"inputs"` 和 `"outputs"` 声明性地描述为 `@app.callback` 装饰器的参数。

```{margin}
关于 `@app.callback` 装饰器

- 通过编写此装饰器，我们告诉 Dash 每当 "input" 组件（文本框）的值更改时为我们调用此函数，以便更新页面上 "output" 组件的子级（HTML div）。
- 您可以为 `@app.callback` 装饰器包装的函数使用任何名称。约定是该名称描述了回调输出。
- 您可以为函数参数使用任何名称，但是必须像在常规 Python 函数中一样在回调函数中使用与定义时相同的名称。参数是位置性的：首先以与装饰器中相同的顺序给出 `Input` 项，然后给出任何  `State` 项。
- 当引用它作为 `@app.callback` 装饰器的输入或输出时，必须使用与给 `app.layout` 中的 Dash 组件相同的 ID。
- `@app.callback` 装饰器需要直接位于回调函数声明的上方。如果装饰器和函数定义之间有空白行，则回调注册将不会成功。
- 如果您对装饰器语法的含义感到好奇，可以阅读此 <a href="https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators/1594484#1594484">StackOverflow 答案</a>，并通过阅读 <a href="https://www.python.org/dev/peps/pep-0318/#current-syntax">PEP 318-函数和方法的装饰器</a> 来了解有关装饰器的更多信息。
```

- 在 Dash 中，我们应用程序的输入和输出只是特定组件的属性。在此示例中，我们的输入是ID为`"my-input"`的组件的`"value"`属性。我们的输出是 ID 为 `"my-output"` 的组件的`"children"`属性。
- 每当输入属性更改时，回调装饰器包装的函数将自动被调用。Dash 为函数提供输入属性的新值作为输入参数，Dash 使用函数返回的值更新输出组件的属性。
- `component_id` 和 `component_property` 关键字是可选的（每个对象只有两个参数）。为了清楚起见，它们包含在此示例中，但是为了简洁和易读起见，在本文档的其余部分中将省略它们。
- 不要混淆 `dash.dependencies.Input` 对象和 `dash_core_components.Input` 对象。前者仅用于这些回调中，而后者是实际组件。
- 注意，我们没有在布局中为 `my-output` 组件的 `children` 属性设置值。Dash 应用程序启动时，它将自动使用输入组件的初始值调用所有回调，以填充输出组件的初始状态。在此示例中，如果您指定了类似 `html.Div(id='my-output', children='Hello world')` 的名称，则在应用启动时它将被覆盖。

这有点像使用 Microsoft Excel 进行编程：每当输入单元格发生更改时，依赖于该单元格的所有单元格都会自动更新。这称为“反应式编程”（"Reactive Programming"）。

还记得每个组件是如何通过其一组关键字参数进行完整描述的吗？这些属性现在很重要。借助 Dash 交互性，我们可以通过回调函数动态更新这些属性中的任何一个。通常，我们将更新组件的 `children` 以显示新文本，或者更新 `dcc.Graph` 组件的 `figure` 以显示新数据，但是我们还可以更新组件的 `style`，甚至更新 `dcc.Dropdown` 组件可用的 `options`！

让我们看一下另一个示例，其中 `dcc.Slider` 更新了 `dcc.Graph`。

## Figure 和 Slider 交互

```{include} ../examples/figure_n_slider.py
:code: python
```

{glue:}`figure_n_slider_dash`

在此示例中，`Slider` 的 `"value"` 属性是应用程序的输入，而应用程序的输出则是 `Graph` 的 `"figure"` 属性。每当 `Slider` 的值更改时，Dash 就会使用新值调用回调函数 `update_figure`。该函数使用此新值过滤数据框，构造一个 `figure` 对象，并将其返回给 Dash 应用程序。

此示例中有一些不错的模式：

1. 我们正在使用 [Pandas](http://pandas.pydata.org/) 库来导入和过滤内存中的数据集。
2. 我们在应用程序的开头加载数据帧：`df = pd.read_csv('...')`。此数据框 `df` 处于应用程序的全局状态，可以在回调函数中读取。
3. 将数据加载到内存中可能会很昂贵。通过在应用程序的开始而不是在回调函数内部加载查询数据，我们确保仅在应用程序服务器启动时执行此操作。当用户访问该应用程序或与该应用程序进行交互时，该数据（`df`）已经在内存中。如果可能，应在应用程序的全局范围内而不是在回调函数内完成昂贵的初始化（如下载或查询数据）。
4. 回调不会修改原始数据，它只是通过 `pandas` 过滤器进行过滤来创建数据帧的副本。这很重要：您的回调函数绝不要在变量范围之外进行变量的更改。如果您的回调修改了全局状态，则一个用户的会话可能会影响下一个用户的会话，并且当应用程序部署在多个进程或线程上时，这些修改将不会在各个会话之间共享。
5. 我们正在使用 `layout.transition` 打开 `transitions`，以了解数据集如何随时间演变：`transitions`允许图表从一个状态平滑地更新到下一个状态，就好像它是动态的一样。

(dash:multiple-inputs)=
## 多输入的回调

在 Dash 中，任何 `"Output"` 可以具有多个 `"Input"` 组件。这是一个简单的示例，它将五个 Inputs（2个`Dropdown`组件，2个`RadioItems`组件和1个`Slider`组件的`value`属性）绑定到1个 Output 组件（`Graph`组件的`figure`属性）。请注意`app.callback`如何在第二个参数的列表内列出所有五个`dash.dependencies.Input`。

```{include} ../examples/multiple_inputs.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/multiple-inputs',
                   className='w3-pale-blue',
                   height=550)
```

在此示例中，只要`Dropdown`，`Slider`或`RadioItems`组件的`value`属性发生更改，就会调用 `update_graph` 函数。

按指定顺序，`update_graph`函数的输入参数是每个`Input`属性的新值或当前值。

即使一次仅更改一个`Input`（用户只能在给定的时刻更改单个`Dropdown`的值），Dash 仍会收集所有指定`Input`属性的当前状态并将其传递给您的函数。您的回调函数始终保证传递给应用程序代表状态。

让我们扩展示例以包括多个输出。

(dash:multiple-outputs)=
## 多输出的回调

到目前为止，我们编写的所有回调仅更新单个`Output`属性。我们也可以一次更新几个：将要更新的所有属性作为列表放置在装饰器中，并从回调中返回那么多项。如果两个输出依赖于相同的计算密集型中间结果（例如慢速数据库查询），则特别好。


```{include} ../examples/multiple_outputs.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
figure_n_slider_dash = Embed(snippet_url + '/examples/multiple-outputs',
                   className='w3-pale-blue',
                   height=280)
figure_n_slider_dash
```

提醒您：即使您可以合并输出，也不总是一个好主意：

- 如果输出依赖于某些而非全部相同的输入，则将它们分开可以避免不必要的更新。
- 如果它们具有相同的输入，但使用这些输入进行独立的计算，则将回调分开设置可以使它们并行运行。

(dash:chained-callback)=
## 链式回调

您也可以将输出和输入链接在一起：一个回调函数的输出可以是另一个回调函数的输入。

此模式可用于创建动态 UI，其中一个输入组件将更新下一个输入组件的可用选项。这是一个简单的例子。


```{include} ../examples/chained_callback.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/chained-callback',
      className='w3-pale-blue',
      height=230)
```

第一个回调根据第一个`RadioItems`组件中的选定值更新第二个`RadioItems`组件中的可用选项。

当`options`属性更改时，第二个回调将设置一个初始值：它将其设置为该`options`数组中的第一个值。

最后的回调显示每个组件的选定`value`。如果更改国家`RadioItems`组件的`value`，则 Dash 将等待，直到更新了城市组件的值，然后才调用最后的回调。这样可以防止以`"America"`和`"Montréal"`之类的不一致状态调用您的回调。

(dash:state-callback)=
## 带状态的 Dash 应用

在某些情况下，您的应用程序中可能会有“表单”类型的模式。在这种情况下，您可能希望读取输入组件的值，但是仅当用户完成了以表格形式输入其所有信息时才可以。

将回调直接附加到输入值可以看起来像这样：

```{include} ../examples/table_callback.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/table-callback',
      className='w3-pale-blue',
      height=60)
```

在此示例中，只要`dash.dependencies.Input`描述的任何属性发生更改，就会触发回调函数。在上面的输入中输入数据，自己尝试一下。

`dash.dependencies.State`允许您传递额外的值而无需触发回调。这是与上述相同的示例，但`dcc.Input`为`dash.dependencies.State`，按钮为`dash.dependencies.Input`。

```{include} ../examples/state_callback.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/state-callback',
      className='w3-pale-blue',
      height=60)
```

在此示例中，在`dcc.Input`框中更改文本不会触发回调，但单击按钮将起作用。`dcc.Input`值的当前值仍会传递到回调中，即使它们不会触发回调函数本身。

请注意，我们通过侦听`html.Button`组件的`n_clicks`属性来触发回调。`n_clicks`是一个属性，每次单击该组件时该属性都会增强。它在`dash_html_components`库中的每个组件中都可用。

## 小结

我们已经介绍了 Dash 中回调的基础。Dash 应用程序是基于一组简单但功能强大的原则构建的：声明性 UI，可通过反应性（reactive）和功能性（functional ）Python 回调进行自定义。声明性组件的每个元素属性都可以通过回调进行更新，并且该属性的子集（例如`dcc.Dropdown`的`value`属性）可以由用户在界面中进行编辑。
