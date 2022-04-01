from dash_extensions.enrich import DashProxy, MultiplexerTransform
import dash_bootstrap_components as dbc
"""
    add the __name__,  otherwise everything is fine locally, but all staff inside the assets folder
    do not work on a server
"""
app = DashProxy(__name__, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
