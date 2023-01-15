from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
import dash
dash.register_page(__name__)

layout = html.Div([
    # 每次刷新页面时，内存存储都会恢复到默认值
    dcc.Store(id='memory'),
    # 本地存储只会在页面第一次加载时获取初始数据，
    # 并一直保存到页面被清除为止。
    dcc.Store(id='local', storage_type='local'),
    # 与本地存储相同，但当浏览器/选项卡关闭时将丢失数据。
    dcc.Store(id='session', storage_type='session'),
    html.Table([
        html.Thead([
            html.Tr(html.Th('点击存储在：', colSpan="3")),
            html.Tr([
                html.Th(html.Button('memory', id='memory-button')),
                html.Th(html.Button('localStorage', id='local-button')),
                html.Th(html.Button('sessionStorage', id='session-button'))
            ]),
            html.Tr([
                html.Th('内存点击'),
                html.Th('本地点击'),
                html.Th('会话点击')
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(0, id='memory-clicks'),
                html.Td(0, id='local-clicks'),
                html.Td(0, id='session-clicks')
            ])
        ])
    ])
])

# 为每个存储创建两个回调
for store in ('memory', 'local', 'session'):
    # 向适当的存储添加一个单击
    @app.callback(Output(store, 'data'),
                  Input(f'{store}-button', 'n_clicks'),
                  State(store, 'data'))
    def on_click(n_clicks, data):
        if n_clicks is None:
            # 阻止 None 回调对存储组件很重要。
            # 您不会想什么也不更新存储。
            raise PreventUpdate
        # 如果没有数据，给出一个默认的数据字典，点击 0 次。
        data = data or {'clicks': 0}
        data['clicks'] = data['clicks'] + 1
        return data

    # 在表格单元格中输出存储的单击。
    @app.callback(Output(f'{store}-clicks', 'children'),
                  # 因为我们在输出中使用了 data 属性，
                  # 所以我们无法通过 data 属性获得加载时的初始数据。为了应对这种情况，
                  # 可以使用 modified_timestamp 作为 Input，使用 data 作为 State。
                  # 这个限制是由于初始的 None 回调
                  # https://github.com/plotly/dash-renderer/pull/81
                  Input(store, 'modified_timestamp'),
                  State(store, 'data'))
    def on_data(ts, data):
        if ts is None:
            raise PreventUpdate
        data = data or {}
        print('data', data)
        return data.get('clicks', 0)
