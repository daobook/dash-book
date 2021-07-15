# Waitress

参考：https://docs.pylonsproject.org/projects/waitress/en/stable/index.html#

Waitress 是一个具有可接受性能的生产质量的纯 Python WSGI 服务器。除了 Python 标准库中的依赖项外，它没有其他依赖项。它在 Python 3.6+ 下运行于 Unix 和 Windows 上的 CPython。它还可以在 UNIX 上的 PyPy 7.3.2 (PyPy3) 上运行。它支持 HTTP/1.0 和 HTTP/1.1。

## 用法

下面的代码将在所有可用 IP 地址（IPv4 和 IPv6）上的 8080 端口上运行。

```python
from waitress import serve
serve(wsgiapp, listen='*:8080')
```

按 `Ctrl-C`（Windows 下按 `Ctrl-Break`）退出服务器。

下面将在 8080 端口上运行所有可用的 IPv4 地址，但不是 IPv6 地址。

```python
from waitress import serve
serve(wsgiapp, host='0.0.0.0', port=8080)
```

默认情况下，Waitress 绑定到 8080 端口上的任何 IPv4 地址。你可以省略 `host` 和 `port` 参数，只用 WSGI 应用作为单个参数调用 `serve`：

```python
from waitress import serve
serve(wsgiapp)
```

如果你想通过 UNIX 域套接字为你的应用提供服务（为下游的 HTTP server/proxy 提供服务，如 nginx, lighttpd 等），使用 `unix_socke`t 参数调用 `serve`：

```python
from waitress import serve
serve(wsgiapp, unix_socket='/path/to/unix.sock')
```

不用说，这种配置在 Windows 上行不通。

默认情况下，由应用程序生成的异常将显示在控制台上。请参见 [Access Logging](https://docs.pylonsproject.org/projects/waitress/en/stable/logging.html#access-logging) 更改此设置。

[PasteDeploy](https://docs.pylonsproject.org/projects/waitress/en/stable/glossary.html#term-pastedeploy)（`egg:waitress#main`）有一个入口点，可以让你从配置文件中使用 Waitress 的 WSGI 网关，例如：

```ini
[server:main]
use = egg:waitress#main
listen = 127.0.0.1:8080
```

也支持使用 `host` 和 `port`：

```ini
[server:main]
host = 127.0.0.1
port = 8080
```

UNIX 域套接字的 PasteDeploy 语法是类似的：

```ini
[server:main]
use = egg:waitress#main
unix_socket = /path/to/unix.sock
```

你可以在 [Arguments to waitress.serve](https://docs.pylonsproject.org/projects/waitress/en/stable/arguments.html#arguments) 找到更多的设置来调整参数。

此外，还有一个命令行运行器叫做 `waitress-serve`，可以在开发中使用，也可以在不需要像 PasteDeploy 这样的情况下使用：

```python
# Listen on both IPv4 and IPv6 on port 8041
waitress-serve --listen=*:8041 myapp:wsgifunc

# Listen on only IPv4 on port 8041
waitress-serve --port=8041 myapp:wsgifunc
```

## Heroku

`Waitress` 可以用来在 Heroku 上提供 WSGI 应用程序，在你的 `requirements.txt` 文件中包含 `waitress`，并将 Procfile 更新如下：

```ini
web: waitress-serve \
    --listen "*:$PORT" \
    --trusted-proxy '*' \
    --trusted-proxy-headers 'x-forwarded-for x-forwarded-proto x-forwarded-port' \
    --log-untrusted-proxy-headers \
    --clear-untrusted-proxy-headers \
    --threads ${WEB_CONCURRENCY:-4} \
    myapp:wsgifunc
```

代理配置通知 Waitress 信任 Heroku 负载均衡器设置的[转发头](https://devcenter.heroku.com/articles/http-routing#heroku-headers)。它还允许设置标准 WEB_CONCURRENCY 环境变量来调整一次由 Waitress 处理的请求数量。

注意 Waitress 使用一个线程模型和仔细的工作应采取确保请求不超过 30 秒或 Heroku 将通知客户端请求失败即使正在处理的请求仍由服务员和占领一个线程，直到它完成。

有关这方面的更多信息，请参见 [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html#runner)。