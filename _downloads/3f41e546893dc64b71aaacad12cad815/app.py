from dash_xinet.server import create_app


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = create_app(__name__,
                 suppress_callback_exceptions=True,
                 external_stylesheets=external_stylesheets,
                 )
