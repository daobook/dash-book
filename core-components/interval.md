(dash:dcc/interval)=
# `dcc.Interval`

`dcc.Interval` 组件会周期性地触发一个回调。使用 `dcc.Interval` 不需要刷新页面或点击任何按钮就可以实时更新应用程序的间隔时间。

其他的例子和策略请参见[实时更新](dash:live-updates)一章。

## `dcc.Interval` 属性

`id`（字符串；可选）：该组件的 ID，用于识别回调中的 Dash 组件。ID 需要在应用程序的所有组件中是唯一的。

`disabled`（布尔值；可选）：如果为 `True`，计数器将不再更新。

`interval`（数字；默认 `1000`）：该组件将每隔 `interval` 毫秒增加计数器 `n_intervals`。

`max_intervals`（数字；默认 `-1`）：间隔将被触发的次数。如果为 `-1`，则该间隔没有限制（默认值），如果为 `0`，则该间隔停止运行。

`n_intervals`（数字；默认 `0`）：间隔经过的次数。