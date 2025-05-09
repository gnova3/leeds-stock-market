import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, page_container  # Only this is required

# Initialize the Dash app
app = dash.Dash(
    __name__,
    use_pages=True,  # Enables automatic page routing from pages/
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Server for gunicorn or flask
server = app.server

# Define app layout
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="user-id", storage_type="session"),
    dbc.NavbarSimple(
        brand="Stock Market Simulation",
        brand_href="#",
        color="primary",
        dark=True,
        fluid=True
    ),
    html.Div(page_container)  # page container renders your page based on pathname
])

if __name__ == "__main__":
    app.run(debug=True)