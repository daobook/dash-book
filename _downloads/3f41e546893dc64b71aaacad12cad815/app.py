from dash_xinet.server import create_app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = create_app(__name__,
                 external_stylesheets=external_stylesheets,
                 )
