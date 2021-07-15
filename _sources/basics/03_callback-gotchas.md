
# 回调 Gotchas

参考：[Callback Gotchas | Dash for Python Documentation | Plotly](https://dash.plotly.com/callback-gotchas)

Dash的工作方式在某些方面可能违反直觉。对于回调系统的工作方式尤其如此。本节概述了在开始构建更复杂的Dash应用程序时可能遇到的一些常见 Dash 陷阱。如果您已经阅读了[Dash教程](https://dash.plotly.com/)的其余部分，并且遇到了意外的行为，那么这是通读的好部分。如果您还有其他问题，可以在[Dash社区论坛](https://community.plotly.com/c/dash)中提问。

## 回调要求其 `Inputs`，`States` 和 `Output`出现在布局中

默认情况下，Dash将验证应用于您的回调，这将执行检查，例如验证回调参数的类型以及检查指定的`Input`和`Output`组件是否实际上具有指定的属性。为了进行全面验证，在您的应用启动时，回调中的所有组件都必须存在于布局中，否则，您将看到错误。

但是，在涉及动态修改布局的更复杂的Dash应用程序（例如多页应用程序）的情况下，并非出现在回调中的每个组件都将包含在初始布局中。您可以通过禁用回调验证来消除此限制，如下所示：

```python
app.config.suppress_callback_exceptions = True
```

## 回调要求在页面上呈现所有 `Inputs` 和 `States`

如果已禁用回调验证以支持动态布局，则不会自动提醒您在布局内未找到回调内组件的情况。在这种情况下，布局中缺少向回调注册的组件，则将无法触发该回调。例如，如果您定义仅在当前页面布局中存在指定`Inputs`的子集的回调，则根本不会触发该回调。

## 组件/属性对只能是一个回调的`Output`

对于给定的组件/属性对（例如`'my-graph'`，`'figure'`），只能将其注册为一个回调的`Output`。如果要将两个逻辑上分开的`Inputs`集与一个输出组件/属性对关联，则必须将它们捆绑成一个更大的回调，并检测哪个相关的`Inputs`触发了函数内的回调。对于`html.Button`元素，可以使用`n_clicks_timestamp`属性来检测是哪个触发了回调。有关此示例，请参阅FAQ中的问题，如何确定哪个输入已更改？

## 必须在服务器启动之前定义所有回调

必须在Dash应用程序的服务器开始运行之前（即在调用`app.run_server(debug=True)`之前）定义所有回调。这意味着，尽管您可以在处理回调过程中动态组装更改后的布局片段，但无法在处理回调过程中定义动态回调来响应用户的输入。如果您具有动态接口，其中回调将布局更改为包括一组不同的输入控件，那么您必须已经预先定义了为这些新控件提供服务所需的回调。

例如，一个常见的场景是一个`Dropdown`组件，该组件会更新当前布局以用另一个逻辑上不同的仪表板替换一个仪表板，该仪表板具有一组不同的控件（控件的数量和类型可能取决于其他用户输入）和不同的逻辑用于生成基础数据。明智的组织应是每个仪表板都具有单独的回调。在这种情况下，每个回调都需要在应用开始运行之前进行定义。

一般而言，如果Dash应用程序的功能是`Inputs`或`States`的数量由用户的输入确定，那么您必须预先预先定义用户可能触发的每个回调排列。有关如何使用`callback`装饰器以编程方式完成此操作的示例，请参见[Dash社区论坛上的帖子](https://community.plotly.com/t/callback-for-dynamically-created-graph/5511)。

## 布局中的所有 Dash Core 组件都应使用回调注册

注意：本部分仅出于遗留目的而存在。在 v0.40.0 之前，仅当组件连接到回调时才定义`setProps`。这就需要像这样在组件内进行复杂的状态管理。现在，始终定义`setProps`，这将简化组件的状态管理。在此[社区论坛主题](https://community.plotly.com/t/callbacks-clearing-all-unconnected-core-components-values/7631)中了解更多信息。

如果布局中存在 Dash Core 组件但未向回调注册（作为`Input`, `State` 或`Output`），则当任何回调更新页面时，用户对其值所做的任何更改都将重置为原始值。

这是一个已知问题，您可以在此[GitHub Issue](https://github.com/plotly/dash-renderer/issues/40)中跟踪其状态。

## 回调定义不需要在列表中

从 Dash 1.15.0 开始，回调定义中的 `Input`，`Output` 和 `State` 不必在列表中。您仍然需要先提供`Output`项，然后提供`Input`项，然后提供`State`，并且仍然支持列表形式。特别是，如果要返回包装在长度为1的列表中的单个`Output`项目，则仍应将输出包装在列表中。这对于过程生成的回调很有用。
