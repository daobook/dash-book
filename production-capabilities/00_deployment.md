# 部署 Dash 应用

参考：[Deploy your Dash App | Dash for Python Documentation | Plotly](https://dash.plotly.com/deployment)

默认情况下，Dash 应用程序运行在本地主机上——你只能在自己的机器上访问它们。要共享 Dash 应用程序，你需要将其“部署”到服务器上。

Dash Enterprise 可以安装在 AWS、Azure、GCP 或[内置 Linux 服务器](https://plotly.com/dash/on-premises-linux/?utm_source=docs&utm_medium=workspace&utm_campaign=nov&utm_content=linux)的 Kubernetes 服务上。[找出你的公司是否在使用 Dash Enterprise](https://go.plotly.com/company-lookup)。

## Heroku 免费分享公共 Dash 应用程序

Heroku 是部署和管理公共 Flask 应用程序最简单的平台之一。Heroku 和 Dash Enterprise 的基于 git 和 buildpack 的 ui 部署几乎是相同的，如果你已经在使用 Heroku，可以轻松过渡到 Dash Enterprise。

查看官方 [Heroku Python](https://devcenter.heroku.com/articles/getting-started-with-python) 指南。

这里有一个简单的例子。这个例子需要一个 Heroku 帐户、`git` 和 `conda`。

### 步骤1：为你的项目创建一个新的文件夹

```sh
$ mkdir dash_app_example
$ cd dash_app_example
```

### 步骤2：使用 `git` 和 `conda` 初始化项目

```sh
$ git init # 初始化 Git 仓库
$ conda create -n dash-book python=3.9 # 创建环境
$ conda activate dash-book # 激活环境
```

安装一些 Python 包：

```sh
$ pip install dash
$ pip install plotly
```

为了部署 Dash，需要安装：

```sh
$ pip install gunicorn
```

### 步骤3：用一个示例 app (`app.py`)、一个 `.gitignore` 文件、`requirements.txt` 和一个用于部署的 `Procfile` 初始化这个文件夹

在项目文件夹中创建以下文件：

`app.py`

:::python
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
:::


`.gitignore`

:::
*.pyc
.DS_Store
:::


`Procfile`

:::
web: gunicorn app:server
:::


```{note}
`app` 指的是文件名 `app.py`。`server` 指的是该文件中的变量 `server`
```

`requirements.txt` 描述了您的 Python 依赖项。你可以自动填写这个文件：

```sh
$ pip freeze > requirements.txt
```

### 步骤四：初始化 Heroku，将文件添加到 Git 中，然后部署

```sh
$ heroku create my-dash-app # change my-dash-app to a unique name
$ git add . # add all files to git
$ git commit -m 'Initial app boilerplate'
$ git push heroku main # deploy code to heroku
$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
```

### 步骤五：更新代码并重新部署

当你用自己的代码修改 `app.py` 时，你需要将这些更改添加到 `git` 中，并将这些更改推到 `heroku` 中。

```sh
$ git status # view the changes
$ git add .  # add all the changes
$ git commit -m 'a description of the changes'
$ git push heroku main
```