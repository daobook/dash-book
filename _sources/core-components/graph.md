---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: ai
  language: python
  name: ai
---

# `dcc.Graph`

参考：[dcc.Graph | Dash for Python Documentation | Plotly](https://dash.plotly.com/dash-core-components/graph)

`dcc.Graph` 组件可用于呈现作为 `figure` 参数传递的任何图形支持的数据可视化。

## Plotly 图形库入门

[Plotly 图形库](https://plotly.com/python/)，即 `plotly` 包，生成“图”。这些是在 `dcc.Graph` 中被使用，例如，`dcc.Graph(figure=fig)` 中的 `fig` 即是 plotly 图。

要开始有条理地学习 plotly，需要了解它的文档是如何组织的：

1. 学习图形的架构：[创建和更新图形](https://plot.ly/python/creating-and-updating-figures/)。
2. 每种图表类型都有一组位于唯一 URL 的示例。熟悉这些页面的结构。例如“Plotly Python柱状图”在 <https://plot.ly/python/histogram>。
3. [Plotly Express](https://plot.ly/python-api-reference/plotly.express.html) 是推荐的高级接口。通过阅读1来理解它。一旦您理解了它的结构，您可以在“API参考”页中看到所有的参数。
4. 图表的每个方面都是可配置的。通读1，了解底层图形界面以及如何修改生成图形的属性。一旦你理解了它，通过访问“[图参考](https://plot.ly/python/reference)”页面来查看所有的属性。
5. 如果你不能用 `px` 轻松生成图形，那么通过阅读1来学习`graph_objects`结构，并通过[图参考](https://plot.ly/python/reference)理解图的结构。

## Plotly Express

`fig` 对象被直接传递到`dcc.Graph`的 `figure` 属性中：

```{code-cell} ipython3

import dash_core_components as dcc
import plotly.express as px

df = px.data.iris() # iris 是 pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

graph = dcc.Graph(figure=fig)
```

```{code-cell} ipython3
:tags: [remove-input]
import plotly.graph_objects as go
# 展示 fig
go.FigureWidget(fig)
```

## 使用带 `go.Figure` 的低级别接口

阅读以上(1)来了解更多关于`px`和`go.Figure`之间的区别。

```{code-cell} ipython3
import plotly.graph_objs as go
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
graph = dcc.Graph(
    id='example-graph-2',
    figure=fig
)
```

```{code-cell} ipython3
:tags: [remove-input]
import plotly.graph_objects as go
# 展示 fig
go.FigureWidget(fig)
```

## 使用带字典和列表的低级别接口

阅读以上(1)来了解更多关于`px`，`go.Figure` 和 `dicts` & `lists` 之间的区别。

```{code-cell} ipython3
import dash_core_components as dcc

fig = {
    'data': [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5],
         'type': 'bar', 'name': u'Montréal'},
    ],
    'layout': {
        'title': r'Dash Data Visualization'
    }
}

graph = dcc.Graph(
    id='example-graph',
    figure=fig
)
```

```{code-cell} ipython3
:tags: [remove-input]
from plotly import io as pio

pio.show(fig)
```

## 交互式图形与回调

[交互式可视化](https://dash.plotly.com/interactive-graphing) 教程解释了如何使用 `dcc.Graph` 捕获用户交互事件，以及如何在回调中更新`figure`属性。

一些高级功能被记录在[社区论坛帖子](https://community.plotly.com/)中：

- 当在回调更新 Graph 时，如何保存 UI 状态（缩放级别等）：[Preserving UI State, like Zoom, in dcc.Graph with uirevision with Dash](https://community.plotly.com/t/preserving-ui-state-like-zoom-in-dcc-graph-with-uirevision-with-dash/15793)
- 图形过渡平滑过渡或图形更新动画：[Exploring a “Transitions” API for dcc.Graph](https://community.plotly.com/t/exploring-a-transitions-api-for-dcc-graph/15468)

## 图形调整和响应性

如果您希望图形的大小具有反应性，那么您可以利用相当多的选项。 

默认的 `plot.js` 行为指示图形应该随着窗口大小的调整而调整大小。但是，在某些情况下，您可能希望根据其父容器的大小来调整图形的大小。（你可以用样式设置父容器的 `style.height` 和 `style.width` 属性。）

`dcc.Graph` 组件的 `responsive` 属性允许你定义你想要的行为。简而言之，它接受 `True`, `False`或 `'auto'` 值：

- `True` 强制图形响应窗口和父窗体的大小调整，而不考虑图中的任何其他 `figure.layout` 或 `config`。
- `False` 强制图形对窗口和父窗口的大小调整无响应，而不考虑图中的任何其他 `figure.layout` 或 `config`。
- `'auto'` 保留遗留行为（大小和大小调整能力由图中指定 `figure.layout` 和 `config.responsive` 的值决定）。

## 如何调整效果（高级）

`dcc.Graph`的属性可以控制图形大小（`responsive` 除外）的图形有：

- `figure.layout.height`：显式设置高度
- `figure.layout.width`：显式设置宽度
- `figure.layout.autosize`：如果为 `True`，则将图形的高度和宽度设置为其父容器的高度和宽度
- `config.responsive`：如果为 `True`，则在窗口大小调整时更改图形的高度和宽度

`responsive` 属性以下列方式与上述属性一起协同：

- `True`：`config.responsive` 和 `figure.layout.autosize` 被 `True` 值覆盖，且 `figure.layout.height` 和 `figure.layout.width` 没有设置
- `False`：`config.responsive` 和 `figure.layout.autosize` 被 `False` 值覆盖
- `'auto'`：plot 的大小决定方式与过去相同（即使用上述四个属性）

## Graph 属性

`id`（字符串；可选）：该组件的 ID，用于识别回调中的 Dash 组件。ID 需要在应用程序的所有组件中是唯一的。

`animate`(布尔；默认为 `False`）：测试版，如果为 `True`，使用 `plot.js` 的 `animate` 函数对动画进行更新处理。

`animation_options`（`dict` 类型；默认 `{ frame: { redraw: False, }, transition: { duration: 750, ease: 'cubic-in-out', },}`）：Beta，包含动画设置的对象。仅当 `animate` 为 `True` 时适用。

`className`（字符串；可选）：父 div 的 `className`。

`clear_on_unhover`(布尔；默认为 `False`）：如果为 `True`, `clear_on_unhover` 将在用户从某个点“解除悬停”时清除 `hoverData` 属性。如果为 `False`，则 `hoverData` 属性将等于从最后一个点开始的悬停数据。

`clickAnnotationData`（`dict` 类型；可选）：来自最新点击注释事件的数据。只读的。

`clickData`（`dict` 类型；可选）：来自最新单击事件的数据。只读的。

`config`（`dict` 类型；可选）：Plotly.js 配置选项。更多信息请参见 [Configuration Options in JavaScript](https://plotly.com/javascript/configuration-options/)。

`config` 是一个带键的字典：

- `autosizable`（布尔值；可选）：无论 `layout.autosize` 如何，都要自动调整一次大小。（否则使用默认的宽度或高度值）
- `displayModeBar`（true, false, 'hover'；可选）：显示模式栏
- `displaylogo`（布尔值；可选）：在模式栏的末尾添加 plotly 徽标
- `doubleClick`（false, 'reset', 'autosize', 'reset+autosize'；可选）：双击交互
- `doubleClickDelay`（数字；可选）：延迟中注册双击事件（毫秒）。最小值为 100，最大值为 1000。默认值是 300。
- `editable`（布尔值；可选）：我们可以编辑标题，移动注释等。设置所有的`edits`片段，除非一个单独的 `edits` 配置项覆盖个别部分。
- `edits`（`dict` 类型；可选）：一组可编辑的属性。
    - `annotationPosition`（布尔值；可选）：注释的主锚，它是文本（如果没有箭头）或箭头（拖动整个东西，使箭头的长度和方向保持不变）。
    - `annotationTail`（布尔值；可选）：对于带箭头的注释，改变箭头的长度和方向。
    - `annotationText`（布尔值；可选）
    - `axisTitleText`（布尔值；可选）
    - `colorbarPosition`（布尔值；可选）
    - `colorbarTitleText`（布尔值；可选）
    - `legendPosition`（布尔值；可选）
    - `legendText`（布尔值；可选）：编辑图例中的轨迹名称字段。
    - `shapePosition`（布尔值；可选）
    - `titleText`（布尔值；可选）：全局 `layout.title`。
- `fillFrame`（布尔值；可选）：如果我们做自动大小，我们是填充容器还是屏幕?
- `frameMargins`（数字；可选）：如果我们要自动调整大小，请以 plot 大小的百分比设置框边距。
- `linkText`（字符串；可选）：出现在 `sendData` 链接中的文本。
- `locale`（字符串；可选）：要使用的区域设置。区域可以通过plot提供（即 `locales`），也可以通过在页面上加载它们，参见：<https://github.com/plotly/plotly.js/blob/master/dist/README.md#to-include-localization>
- `locales`（`dict` 类型；可选）：本地化定义，如果您选择为它们提供图形，而不是全局注册它们。
- **`mapboxAccessToken`** (*boolean | number | string | dict | list*; optional): Mapbox access token (required to plot mapbox trace types) If using an Mapbox Atlas server, set this option to '', so that plotly.js won't attempt to authenticate to the public Mapbox server.
- **`modeBarButtons`** (*boolean | number | string | dict | list*; optional): Fully custom mode bar buttons as nested array, where the outer arrays represents button groups, and the inner arrays have buttons config objects or names of default buttons.
- **`modeBarButtonsToAdd`** (*list*; optional): Add mode bar button using config objects.
- **`modeBarButtonsToRemove`** (*list*; optional): Remove mode bar button by name. All modebar button names at [https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js](https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js) Common names include: sendDataToCloud; (2D) zoom2d, pan2d, select2d, lasso2d, zoomIn2d, zoomOut2d, autoScale2d, resetScale2d; (Cartesian) hoverClosestCartesian, hoverCompareCartesian; (3D) zoom3d, pan3d, orbitRotation, tableRotation, handleDrag3d, resetCameraDefault3d, resetCameraLastSave3d, hoverClosest3d; (Geo) zoomInGeo, zoomOutGeo, resetGeo, hoverClosestGeo; hoverClosestGl2d, hoverClosestPie, toggleHover, resetViews.
- **`plotGlPixelRatio`** (*number*; optional): Increase the pixel ratio for Gl plot images.
- **`plotlyServerURL`** (*string*; optional): Base URL for a Plotly cloud instance, if `showSendToCloud` is enabled.
- **`queueLength`** (*number*; optional): Set the length of the undo/redo queue.
- **`responsive`** (*boolean*; optional): Whether to change layout size when the window size changes.
- **`scrollZoom`** (*boolean*; optional): Mousewheel or two-finger scroll zooms the plot.
- **`sendData`** (*boolean*; optional): If we show a link, does it contain data or just link to a plotly file?.
- **`showAxisDragHandles`** (*boolean*; optional): Enable axis pan/zoom drag handles.
- **`showAxisRangeEntryBoxes`** (*boolean*; optional): Enable direct range entry at the pan/zoom drag points (drag handles must be enabled above).
- **`showEditInChartStudio`** (*boolean*; optional): Should we show a modebar button to send this data to a Plotly Chart Studio plot. If both this and showSendToCloud are selected, only showEditInChartStudio will be honored. By default this is False.
- **`showLink`** (*boolean*; optional): Link to open this plot in plotly.
- **`showSendToCloud`** (*boolean*; optional): Should we include a modebar button to send this data to a Plotly Cloud instance, linked by `plotlyServerURL`. By default this is False.
- **`showTips`** (*boolean*; optional): New users see some hints about interactivity.
- **`staticPlot`** (*boolean*; optional): No interactivity, for export or image generation.
- `toImageButtonOptions` (dict; optional): Modifications to how the toImage modebar button works.
    `toImageButtonOptions` is a dict with keys:
    - `filename` (string; optional): The name given to the downloaded file.
    - `format` (a value equal to: 'jpeg', 'png', 'webp', 'svg'; optional): The file format to create.
    - `height` (number; optional): Height of the downloaded file, in px.
    - `scale` (number; optional): Extra resolution to give the file after rendering it with the given width and height.
    - `width` (number; optional): Width of the downloaded file, in px.
- `topojsonURL` (string; optional): URL to topojson files used in geo charts.
- `watermark` (boolean; optional): Add the plotly logo even with no modebar.

**`extendData`** (*list | dict*; optional): Data that should be appended to existing traces. Has the form `[updateData, traceIndices, maxPoints]`, where `updateData` is an object containing the data to extend, `traceIndices` (optional) is an array of trace indices that should be extended, and `maxPoints` (optional) is either an integer defining the maximum number of points allowed or an object with key:value pairs matching `updateData` Reference the Plotly.extendTraces API for full usage: [https://plotly.com/javascript/plotlyjs-function-reference/#plotlyextendtraces](https://plotly.com/javascript/plotlyjs-function-reference/#plotlyextendtraces).

**`figure`** (*dict*; default `{ data: \[\], layout: {}, frames: \[\],}`): Plotly `figure` object. See schema: [https://plotly.com/javascript/reference](https://plotly.com/javascript/reference) `config` is set separately by the `config` property.

`figure` is a dict with keys:

- **`data`** (*list of dicts*; optional)

- **`frames`** (*list of dicts*; optional)

- **`layout`** (*dict*; optional)

**`hoverData`** (*dict*; optional): Data from latest hover event. Read-only.

**`loading_state`** (*dict*; optional): Object that holds the loading state object coming from dash-renderer.

`loading_state` is a dict with keys:

- **`component_name`** (*string*; optional): Holds the name of the component that is loading.

- **`is_loading`** (*boolean*; optional): Determines if the component is loading or not.

- **`prop_name`** (*string*; optional): Holds which property is loading.

**`prependData`** (*list | dict*; optional): Data that should be prepended to existing traces. Has the form `[updateData, traceIndices, maxPoints]`, where `updateData` is an object containing the data to prepend, `traceIndices` (optional) is an array of trace indices that should be prepended, and `maxPoints` (optional) is either an integer defining the maximum number of points allowed or an object with key:value pairs matching `updateData` Reference the Plotly.prependTraces API for full usage: [https://plotly.com/javascript/plotlyjs-function-reference/#plotlyprependtraces](https://plotly.com/javascript/plotlyjs-function-reference/#plotlyprependtraces).

**`relayoutData`** (*dict*; optional): Data from latest relayout event which occurs when the user zooms or pans on the plot or other layout-level edits. Has the form `{<attr string>: <value>}` describing the changes made. Read-only.

**`responsive`** (*a value equal to: true, false, 'auto'*; default `'auto'`): If True, the Plotly.js plot will be fully responsive to window resize and parent element resize event. This is achieved by overriding `config.responsive` to True, `figure.layout.autosize` to True and unsetting `figure.layout.height` and `figure.layout.width`. If False, the Plotly.js plot not be responsive to window resize and parent element resize event. This is achieved by overriding `config.responsive` to False and `figure.layout.autosize` to False. If 'auto' (default), the Graph will determine if the Plotly.js plot can be made fully responsive (True) or not (False) based on the values in `config.responsive`, `figure.layout.autosize`, `figure.layout.height`, `figure.layout.width`. This is the legacy behavior of the Graph component. Needs to be combined with appropriate dimension / styling through the `style` prop to fully take effect.

**`restyleData`** (*list*; optional): Data from latest restyle event which occurs when the user toggles a legend item, changes parcoords selections, or other trace-level edits. Has the form `[edits, indices]`, where `edits` is an object `{<attr string>: <value>}` describing the changes made, and `indices` is an array of trace indices that were edited. Read-only.

**`selectedData`** (*dict*; optional): Data from latest select event. Read-only.

**`style`** (*dict*; optional): Generic style overrides on the plot div.
