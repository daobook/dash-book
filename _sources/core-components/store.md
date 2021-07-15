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

(dash:dcc/store)=
# `dcc.Store`

参考：[dcc.Store | Dash for Python Documentation | Plotly](https://dash.plotly.com/dash-core-components/store)

`dcc.Store` 组件用于在浏览器中存储 JSON 数据。

## 点击的例子

```{include} ../examples/store_clicks.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]
        
from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/store-clicks',
      className='w3-pale-blue',
      height=210)
```

## 在回调之间共享数据

```{include} ../examples/share_data_callbacks.py
:code: python
```

```{code-cell} ipython3
:tags: [remove-input]

from sanstyle.display.html import Embed

snippet_url = 'https://dash-book.herokuapp.com'
Embed(snippet_url + '/examples/share-data-callbacks',
      className='w3-pale-blue',
      height=800)
```

## Storage 的限制

- 浏览器的最大存储空间由以下因素决定：
  - 手机或笔记本电脑。
  - 在浏览器中，一个复杂的算法在配额管理（Quota Management）中实现。
  - UTF-16 的存储编码最终只能节省 UTF-8 的一半大小。
  - 一般来说，在大多数环境中存储 2MB 是安全的，而在大多数只有桌面的应用程序中存储 5~10MB 是安全的。
- `modified_timestamp` 为只读。

## 检索初始存储数据

如果使用 `data` 属性作为输出，则无法使用 `data` 属性获得加载时的初始数据。为了应对这种情况，可以使用 `modified_timestamp` 作为 `Input`，使用 `data` 作为 `State`。

## `dcc.Store` 属性

`id`（字符串；必需）：此组件的 ID，用于在回调中识别 Dash 组件。ID 需要在应用程序的所有组件中是唯一的。
- `clear_data`（布尔；默认 `False`）：设置为 `True` 删除 `data_key` 中包含的数据。
- `data`（dict | list | number | string | boolean；可选）：`id` 的存储数据。
- `modified_timestamp`（数字；默认 `-1`）：上次修改存储的时间。
- `storage_type`（'local', 'session', 'memory'（默认））：网络存储的类型。`memory`：只保留在内存中，刷新页面时重置。` local`：`window.localStorage`，浏览器退出后保留数据。`session`：window.sessionStorage，一旦浏览器退出，数据将被清除。