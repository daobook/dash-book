(dash:dcc/location)=
# `dcc.Location`

`dcc.Location` 组件表示 web 浏览器中的位置或地址栏。通过它的 `href`, `pathname`, `search` 和 `hash` 属性，你可以访问应用程序加载的 url 的不同部分。

更多细节请参阅 [](dash:urls) 章节。

例如，给定 url `http://127.0.0.1:8050/page-2?a=test#quiz`，有：

- `href` = `"http://127.0.0.1:8050/page-2?a=test#quiz"`
- `pathname` = `"/page-2"`
- `search` = `"?a=test"`
- `hash` = `"#quiz"`

`id`（字符串；可选）：此组件的 ID，用于在回调中识别 Dash 组件。ID 需要在应用程序的所有组件中是唯一的。

`hash`（字符串；可选）：`window.location` 中的 `hash`，例如，`"#myhash"`。

`href`（字符串；可选）：`window.location` 中的 `href`，例如，`"/my/full/pathname?myargument=1#myhash"`。

`pathname`（字符串；可选）：`window.location` 中的 `pathname`，例如，`"/my/full/pathname"`。

`refresh`（布尔值；默认 `True`）：更新位置时是否刷新页面。

`search`（字符串；可选）：`window.location` 中的 `search`，例如，`"?myargument=1"`。