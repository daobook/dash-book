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

(dash:performance)=
# 性能

参考：[Performance | Dash for Python Documentation | Plotly](https://dash.plotly.com/performance)

本章包含了一些改进你的 Dash 应用程序性能的建议。

Dash 应用程序的主要性能限制可能是应用程序代码本身的回调。如果你能加快回调的速度，你的应用程序会感觉更轻快。

## 记忆化

因为 Dash 的回调本质上是函数性的（它们不包含任何状态），所以很容易添加记忆缓存。内存保存函数被调用后的结果，并在使用相同参数调用函数时重用结果。

关于在 Dash 应用中使用记忆来提高性能的简单例子，请参阅高级回调章节中的“[用记忆提高性能](dash:advanced-callbacks/memoization)”一节。

Dash 应用程序经常跨多个进程或线程部署。在这些情况下，每个进程或线程包含自己的内存，它不跨实例共享内存。这意味着如果我们使用 `lru_cache`，缓存的结果可能不会在会话之间共享。

相反，我们可以使用 [Flask-Caching](https://pythonhosted.org/Flask-Caching/) 库，它将结果保存在一个像 Redis 这样的共享内存数据库中，或者作为文件保存在你的文件系统中。Flask-Caching 还有其他一些不错的特性，比如基于时间的逾时（expiry）。如果你想每小时或每天更新你的数据（清除你的缓存），基于时间的逾时是有用的。

下面是一个使用 Redis 的 Flask-Caching 的例子：

```{include} ../examples/flask_caching.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]

from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/flask-caching',
      className='w3-pale-blue',
      height=120)
```

下面是一个**缓存数据集**而不是回调的例子。它使用 FileSystem 缓存，将缓存的结果保存到文件系统。

如果有一个数据集用于更新多个回调，那么这种方法很有效。

```{include} ../examples/caching_dataset.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]

from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/caching-dataset',
      className='w3-pale-blue',
      height=520)
```

## Graphs

[Plotly.js](https://github.com/plotly/plotly.js) 开箱即用非常快。

大多数图形都是用 SVG 呈现的。这提供了清晰的渲染、发布质量的图像导出和广泛的浏览器支持。不幸的是，对于大型数据集（比如那些超过 15k 点的数据集），SVG 呈现图形可能很慢。为了克服这个限制，` plotly.js` 提供了一些图表类型的 WebGL 替代方案。WebGL 使用 GPU 渲染图形。

高性能的 WebGL 替代品包括：

- `scattergl`：`scatter` 图类型的 webgl 实现。[Examples](https://plotly.com/python/webgl-vs-svg/) & [reference](https://plotly.com/python/reference/#scattergl)
- `pointcloud`：一个轻量级版本的 `scattergl` 具有有限的可定制性，但甚至更快的渲染。[Reference](https://plotly.com/python/reference/#pointcloud)
- `heatmapgl`：`heatmap` 类型的 webgl 实现。[Reference](https://plotly.com/python/reference/#heatmapgl)

：目前，dash 在更新时使用 `plotly.js` 的 `newPlot` 回调重新绘制整个图形。通过在此逻辑中引入 `restyle` 回调，可以显著提高更新图表的性能。

## 客户端回调

客户端回调以 JavaScript 在客户端执行代码，而不是以 Python 在服务器端执行代码。

更多关于客户端回调的信息，请参阅 [客户端回调](dash:clientside-callbacks) 一章。