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

(dash:dcc/range-slider)=
# `dcc.RangeSlider`

参考：[dcc.RangeSlider | Dash for Python Documentation | Plotly](https://dash.plotly.com/dash-core-components/rangeslider)

## 简单例子

一个绑定回调的基本 RangeSlider 的例子。


```{include} ../examples/simple_range_slider.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/simple-range-slider',
      className='w3-pale-blue',
      height=100)
```

## 标记和步长

如果滑块 `marks` 被定义并且 `step` 被设置为 `None`，那么滑块将只能选择标记预定义的值。注意，默认值是 `step=1`，因此必须显式指定 `None` 以获得此行为。

```{include} ../examples/mark_range_slider.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/mark-range-slider',
      className='w3-pale-blue',
      height=100)
```

待续。。。