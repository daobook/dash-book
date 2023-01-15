from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import no_update

from app import app
import dash
dash.register_page(__name__)
layout = html.Div([
    html.P('输入一个合数以查看它的质因数'),
    dcc.Input(id='num', type='number', debounce=True, min=1, step=1),
    html.P(id='err', style={'color': 'red'}),
    html.P(id='out')
])


@app.callback(
    Output('out', 'children'),
    Output('err', 'children'),
    Input('num', 'value')
)
def show_factors(num):
    if num is None:
        # PreventUpdate 阻止所有输出更新
        raise PreventUpdate

    factors = prime_factors(num)
    if len(factors) == 1:
        # no_update 防止任何单个输出更新
        # (注意:它也可以用于单输出回调)
        return no_update, f'{num} is prime!'

    return f"{num} 是 {' * '.join(str(n) for n in factors)}", ''


def prime_factors(num):
    n, i, out = num, 2, []
    while i ** 2 <= n:
        if n % i == 0:
            n = int(n / i)
            out.append(i)
        else:
            i += 1 if i == 2 else 2
    out.append(n)
    return out
