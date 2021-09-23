# Dash 简介

参考：[Introduction | Dash for Python Documentation | Plotly](https://dash.plotly.com/introduction)

Dash 通过一些简单的模式，抽象出构建一个基于 Web 的交互式应用程序所需的所有技术和协议。Dash 非常简单，您可以在一个下午就将用户界面绑定到您的 Python 代码中。

Dash 应用程序在网络浏览器中呈现。您可以将应用程序部署到服务器上，然后通过 URL 共享它们。由于 Dash 应用是在网页浏览器中查看的，因此 Dash 天生就具备跨平台和移动功能。

Dash 应用程序由两部分组成：

1. 应用程序的布局。它描述了应用程序的外观。
2. 应用程序的交互性。

## 安装

在你的终端，安装 `dash`：

```sh
pip install dash
```

这带来了构成 Dash 核心的三个组件库：`dash_html_components`、`dash_core_components`、`dash_table` 以及 `plotly` 图形库。这些库正在积极开发中，所以要经常安装和升级。

如果喜欢使用 [Jupyter 笔记本](https://plotly.com/dash/workspaces/?tab=jupyter-notebooks) 或 JupyterLab 作为你的开发环境，建议安装 [`jupyter-dash`](https://github.com/plotly/jupyter-dash)：

```sh
conda install -c conda-forge -c plotly jupyter-dash
```

Dash 为应用程序的所有可视化组件提供了 Python 类。在 `dash_core_components` 和 `dash_html_components` 库中维护了一组组件，但也可以用 JavaScript 和 React.js [构建自己的组件](https://github.com/plotly/dash-component-boilerplate)。

注意：在本书中，使用 Jupyter 环境。
