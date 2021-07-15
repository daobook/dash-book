
# FAQs

参考：[Part 6\. FAQs | Dash for Python Documentation | Plotly](https://dash.plotly.com/faqs)

问：如何自定义 Dash 应用程序的外观？
答：Dash 应用程序在浏览器中呈现为符合现代标准的 Web 应用程序。这意味着您可以像使用标准 HTML 一样使用 CSS 来设置 Dash 应用的样式。

所有`dash-html-components`都通过`style`属性支持内联 CSS 样式。通过定位组件的 ID 或类名称，外部 CSS 样式表还可用于设置`dash-html-components`和`dash-core-components`的样式。`dash-html-components`和`dash-core-components`都接受属性`className`，该属性对应于 HTML 元素属性类。

[Dash HTML Components](https://dash.plotly.com/dash-html-components) 中的“Dash HTML组件”部分说明了如何为`dash-html-components`提供内联样式和 CSS 类名，您可以使用 CSS 样式表作为目标。Dash指南中的[Adding CSS & JS and Overriding the Page-Load Template](https://dash.plotly.com/external-resources)部分说明了如何将自己的样式表链接到 Dash 应用。

----

问：如何将 JavaScript 添加到 Dash 应用程序？
答：您可以将自己的脚本添加到 Dash 应用程序中，就像将 JavaScript 文件添加到 HTML 文档中一样。请参阅《Dash 指南》中的[Adding CSS & JS and Overriding the Page-Load Template](https://dash.plotly.com/external-resources)部分。

----

问：我可以制作包含多个页面的 Dash 应用程序吗？
答：是的！Dash 支持多页应用程序。请参阅《Dash用户指南》中的[Multi-Page Apps and URL Support](https://dash.plotly.com/urls)部分。

----

问：如何将 Dash 应用程序组织成多个文件？
答：可以在《Dash用户指南》的[Multi-Page Apps and URL Support](https://dash.plotly.com/urls)部分中找到执行此操作的策略。

---

问：如何确定哪个输入已更改？
答：请参阅[Advanced Callbacks](https://dash.plotly.com/advanced-callbacks)部分中的`dash.callback_context`。

---

问：我可以将 Jinja2 模板与 Dash 一起使用吗？

答：Jinja2 模板在作为 HTML 页面发送到客户端之前，先在服务器上呈现（通常在 Flask 应用程序中）。另一方面，Dash 应用程序是使用 React 在客户端上呈现的。这使这些在浏览器中显示 HTML 的方法截然不同，这意味着这两种方法无法直接组合。但是，您可以将 Dash 应用程序与现有的 Flask 应用程序集成在一起，以便 Flask 应用程序可以处理某些 URL 端点，而 Dash 应用程序位于特定的 URL 端点。

---


问：我可以将 jQuery 与 Dash 一起使用吗？

答：在大多数情况下，您不能这样做。Dash 使用 React 在客户端浏览器上呈现您的应用程序。React 与 jQuery的根本不同之处在于，它利用虚拟 DOM（文档对象模型）来管理页面呈现。由于 jQuery 不会讲 React 的虚拟DOM，因此您无法使用 jQuery 的任何 DOM 操作工具来更改页面布局，这经常就是为什么要使用 jQuery 的原因。但是，您可以使用 jQuery 功能中不接触 DOM 的部分，例如注册事件侦听器以使击键导致页面重定向。

通常，如果您希望在应用程序中添加自定义客户端行为，我们建议将该行为封装在[自定义 Dash 组件](https://dash.plotly.com/plugins)中。

----

问：那些很棒的撤消和重做按钮去哪了？

答：好的，主要是我们遇到了相反的问题：[How do I get rid of the undo/redo buttons](https://community.plotly.com/t/is-it-possible-to-hide-the-floating-toolbar/4911/10)。尽管从技术角度来看此功能很简洁，但大多数人在实践中并不认为它有价值。从 Dash 1.0 开始，默认情况下会删除按钮，不需要任何怪异的 CSS 技巧。如果您想让他们回来，请使用 `show_undo_redo`：

```python
app = Dash(show_undo_redo=True)
```

---

问：我还有其他问题！我在哪里可以问他们？
答：[Dash 社区论坛](https://community.plotly.com/c/dash)上挤满了讨论 Dash 主题，互相帮助的人以及共享Dash创作的人。跳过并加入讨论。