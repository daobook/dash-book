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

# 交互式可视化

参考：[Part 4\. Interactive Graphing and Crossfiltering | Dash for Python Documentation | Plotly](https://dash.plotly.com/interactive-graphing)

`dash_core_components`库包含一个名为`Graph`的组件。

`Graph`使用开源 [`plotly.js`](https://github.com/plotly/plotly.js) JavaScript 图形库呈现交互式数据可视化。`plotly.js` 支持超过 35 种图表类型，并以矢量质量 SVG 和高性能 WebGL 呈现图表。

`dash_core_components.Graph`组件中的 `figure` 参数与 Plotly 的开源 Python 图形库 `plotly.py` 使用的图形参数相同。请查看 [plotly.py 文档和画廊](https://plotly.com/python) 以了解更多信息。

Dash 组件通过一组属性声明性地描述。所有这些属性都可以通过回调函数进行更新，但是这些属性的子集只能通过用户交互来更新，例如，当您单击`dcc.Dropdown`组件中的某个选项时，该组件的`value`属性将发生更改。

`dcc.Graph`组件具有四个可以通过用户交互更改的属性：`hoverData`，`clickData`，`selectedData`，`relayoutData`。当您将鼠标悬停在点上，单击点或选择图形中的点区域时，这些属性会更新。

为了获得最佳的用户交互和图表加载性能，生产环境的 Dash 应用程序应考虑 Dash Enterprise 的 [Job Queue](https://plotly.com/dash/job-queue), [HPC](https://plotly.com/dash/big-data-for-python), [Datashader](https://plotly.com/dash/big-data-for-python), 和 [horizontal scaling](https://plotly.com/dash/kubernetes)。

````{dropdown} 这是一个在屏幕上打印这些属性的简单示例。

```{include} ../examples/print_graph.py
:code: python
```
````

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/print-graph',
      className='w3-pale-blue',
      height=800)
```

## 悬停更新图

````{dropdown} 当我们将鼠标悬停在散点图中的点上时，让我们通过更新时间序列来更新上一章中的世界指标示例。
```{include} ../examples/hover_update_graph.py
:code: python
```
````

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/hover-update-graph',
      className='w3-pale-blue',
      height=600)
```

尝试将鼠标悬停在左侧散点图中的点上。请注意，右侧的折线图是如何根据您悬停的点进行更新的。

## 通用交叉过滤食谱

````{dropdown} 这是对六列数据集进行交叉过滤的更通用的示例。每个散点图的选择都会过滤基础数据集。
```{include} ../examples/cross_filter.py
:code: python
```
````

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/cross-filter',
      className='w3-padding',
      height=500)
```

尝试单击并拖动任何图以过滤不同区域。在每次选择时，将使用每个图的最新选定区域触发三个图形回调。根据所选点过滤熊猫数据帧，并以突出显示所选点的方式重新绘制图形，并将所选区域绘制为虚线矩形。

>顺便说一句，如果您发现自己过滤和可视化高维数据集，则应考虑检查 [并行坐标图表类型](https://plotly.com/python/parallel-coordinates-plot/)。

## 当前的局限性

目前，图形交互存在一些限制。

- 当前无法自定义悬停交互或选择框的样式。这个问题正在 <https://github.com/plotly/plotly.js/issues/1847> 中处理。

这些交互式绘图功能可以做很多事情。如果需要帮助来探索用例，请在 [Dash 社区论坛](https://community.plotly.com/c/dash) 中打开一个线程。
