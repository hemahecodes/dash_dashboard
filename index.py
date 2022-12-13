from dash import html, dcc
from dash.dependencies import Input, Output
from page_1 import app_layout
from main import app


server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    app_layout()
])


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
