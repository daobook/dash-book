# 关于 Plotly Dash 你需要知道的一切

```{describe} 参考
[Plotly Dash — Everything You Need To Know | by Stephen Kilcommins | DataDrivenInvestor](https://medium.datadriveninvestor.com/plotly-dash-everything-you-need-to-know-bc09a5e45395)
```

{term}`Dash` 是在 Flask, Plotly.js 和 React.js 之上编写的。它允许用户使用常规 Python 创建交互式仪表板，而不必担心后端代码、路由和请求。Dash 在浏览器中呈现，使其成为一个跨平台的解决方案。Dash 是一个与语言无关的框架——支持 Python、R 和 Julia 编程语言。

## 支持 Python 图形库

用于在 Dash 中创建图形的“[Graph](https://dash.plotly.com/dash-core-components/graph)”组件将 Plotly 图形作为输入，这意味着 Dash 主要是为使用 “`plotly.py`” Python 图形库而构建的。Dash 中存在用于显示可选 Python 绘图库的外部库，即 Seaborn/Matplotlib、Altair/Vega-Lite 和 Bokeh，但是这些库不是很健壮，并且与输出图的交互水平与 Plotly 生成的图不在同一水平上。

在 Dash 中用于与其他绘图库一起工作的主要 Python 库称为 “[Dash -alternative-viz](https://github.com/plotly/dash-alternative-viz)”。如果您选择使用 Dash，建议主要使用 Plotly 图，因为框架是在考虑它们的情况下构建的。

## 多页面应用程序支持

Dash 显式支持多页面应用程序。它还可以在不刷新实际网页的情况下改变 URL，从而在页面之间快速导航，大大减少了页面加载时间。[Dash 用户指南](https://dash.plotly.com/introduction) 本身就是一个多页面 Dash 应用程序的例子。

虽然 Dash 以一种性能方式处理多页面应用程序，但在多页面应用程序中使用 Dash 的一个主要警告是，Dash 框架是无状态的，这限制了多页面应用程序的实现，因为状态不能在服务器端单独的页面之间共享。

## 安装和入门

在你的终端，安装 `dash`：

```shell
pip install dash
```

此安装包包含构成 Dash 核心的三个组件库：`dash_html_components`、`dash_core_components`、`dash_table` 以及 `plotly` 图形库。

如果你喜欢使用  [Jupyter Notebook](https://plotly.com/dash/workspaces/?tab=jupyter-notebooks) 或 JupyterLab 作为你的开发环境，我们建议安装 [jupyter-dash](https://github.com/plotly/jupyter-dash)：

```shell
pip install jupyter-dash
```

`jupyter-dash` 库可以很容易地从 Jupyter 环境（例如经典的笔记本，木星实验室，Visual Studio 代码笔记本，nteract，PyCharm 笔记本等）开发 Plotly Dash 应用程序交互。

> 在开始开发 Dash 应用程序时，这里有一个次要的学习曲线，为了真正找到你的立足点，你应该学习这个指南，而不是快速浏览。建议在开始创建你的第一个 Dash 应用程序之前，先彻底阅读一下这个教程指南以及 [Dash 核心组件概述](https://dash.plotly.com/dash-core-components) 和 [Dash HTML 组件概述](https://dash.plotly.com/dash-html-components)。

你可以在这里找到一些 [Dash 应用程序的例子](https://dash-gallery.plotly.host/Portal/)，以及相应的[应用程序源代码](https://github.com/plotly/dash-sample-apps/)。

## Dash

- [Integrate machine learning and big data into real-time business intelligence with Snowflake and Plotly’s Dash | by plotly | Plotly | Medium](https://medium.com/plotly/integrate-machine-learning-and-big-data-into-real-time-business-intelligence-with-snowflake-and-c972b5ea274e)
- [Productionizing Object Detection Models with Dash Enterprise | by plotly | Plotly | Medium](https://medium.com/plotly/productionizing-object-detection-models-with-dash-enterprise-dba1c9402c2f)

## 部署

参考 [The Easiest Way to Deploy Your Dash App for Free | by Elsa Scola | Towards Data Science](https://towardsdatascience.com/the-easiest-way-to-deploy-your-dash-app-for-free-f92c575bb69e) & [Plotly Dash apps: Deploy Instantly with Zero Configuration | by Dan Lester | Analytics Vidhya | Medium](https://medium.com/analytics-vidhya/plotly-dash-apps-deploy-instantly-with-zero-configuration-fe1e5730763d)。

## 菜单

- [plotly/dash-recipes: A collection of scripts and examples created while answering questions from the greater Dash community (github.com)](https://github.com/plotly/dash-recipes)
- [Plotly – Medium](https://medium.com/plotly)
- [Part II: Deploying a Dash Application to Operationalize Machine Learning Models | by plotly | Plotly | Medium](https://medium.com/plotly/part-ii-deploying-a-dash-application-to-operationalize-machine-learning-models-643eab4e2905)
- [Plotly and NVIDIA Partner to Integrate Dash and RAPIDS | by plotly | Plotly | Medium](https://medium.com/plotly/plotly-and-nvidia-partner-to-integrate-dash-and-rapids-8a8c53cd7daf)
- [Introducing Dash HoloViews. We’re happy to announce the release of… | by Jon Mease | Plotly | Medium](https://medium.com/plotly/introducing-dash-holoviews-6a05c088ebe5)
- [How AE Studio built a better software estimation tool on Dash Enterprise | by Amélie Beurrier | Plotly | Medium](https://medium.com/plotly/how-ae-studio-built-a-better-software-estimation-tool-on-dash-enterprise-a89f3f9644de)
- [Introducing Kaleido ✨. Static image export for web-based… | by Jon Mease | Plotly | Medium](https://medium.com/plotly/introducing-kaleido-b03c4b7b1d81)
- [Building and Deploying Explainable AI Dashboards using Dash and SHAP | by Xing Han Lu | Plotly | Medium](https://medium.com/plotly/building-and-deploying-explainable-ai-dashboards-using-dash-and-shap-8e0a0a45beb6)
- [Interactive and scalable dashboards with Vaex and Dash | by Jovan Veljanoski | Plotly | Medium](https://medium.com/plotly/interactive-and-scalable-dashboards-with-vaex-and-dash-9b104b2dc9f0)
- [Building apps for editing Face GANs with Dash and Pytorch Hub | by plotly | Plotly | Medium](https://medium.com/plotly/building-apps-for-editing-face-gans-with-dash-and-pytorch-hub-1e7026c0bc9a)
- [Dash is an ideal Python based front-end for your Databricks Spark Backend | by plotly | Plotly | Medium](https://medium.com/plotly/dash-is-an-ideal-front-end-for-your-databricks-spark-backend-212ee3cae6cc)
- [Beyond “tidy”: Plotly Express now accepts wide-form and mixed-form data | by Nicolas Kruchten | Plotly | Medium](https://medium.com/plotly/beyond-tidy-plotly-express-now-accepts-wide-form-and-mixed-form-data-bdc3e054f891)
