import dash
from dash import Dash
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR],
           use_pages=False,
           prevent_initial_callbacks=True,
           suppress_callback_exceptions=True)
