(dash:dcc/link)=
# `dcc.Link`

要了解更多关于链接的信息，请参阅 [Dash url](dash:urls) 这一章。

`children`（由单独的 Dash 组件、字符串或数字组成的列表；可选）：该组件的子组件。

`id`（字符串；可选）：此组件的 ID，用于在回调中识别 Dash 组件。ID 需要在应用程序的所有组件中是唯一的。

`className`（字符串；可选）：通常与 CSS 一起使用，以样式化具有公共属性的元素。

`href`（字符串；必需）：链接资源的 URL。

`loading_state`（dict；可选）：持有来自 `dash-renderer` 的加载状态对象的对象。

`loading_state` 的关键字：

- `component_name`（字符串；可选）：保存正在加载的组件的名称。
- `is_loading`（布尔值；可选）：确定组件是否正在加载。
- `prop_name`（字符串；可选）：保存正在加载的属性。

`refresh`（布尔值；默认 `False`）：控制单击链接时页面是否会刷新。

`style`（dict；可选）：定义将覆盖以前设置的样式的 CSS 样式。

`target`（字符串；可选）：指定在何处打开链接引用。

`title`（字符串；可选）：向链接添加标题属性，可以包含补充信息。