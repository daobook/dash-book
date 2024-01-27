from dash_xinet.server import create_app


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = create_app(__name__,
                 external_stylesheets=external_stylesheets,
                 )
