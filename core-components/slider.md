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

(dash:dcc/slider)=
#  `dcc.Slider`

一个绑定回调的基本滑块的例子。

```{include} ../examples/simple_slider.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-tests.herokuapp.com'
Embed(snippet_url + '/examples/simple-slider',
      className='w3-pale-blue',
      height=70)
```