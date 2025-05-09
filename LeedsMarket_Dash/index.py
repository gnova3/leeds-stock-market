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

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="user-id", storage_type="session"),
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Leeds Stock Market Simulation", style={"fontSize": "32px", "fontWeight": "bold", "margin": "0 auto"})
        ]),
        color="primary",
        dark=True,
        sticky="top"
    ),
    html.Div(page_container, className="flex-grow-1 px-5"),
    html.Footer(
        "Choice Modelling Centre — University of Leeds",
        className="text-center text-white py-3 bg-primary mt-auto"
    )
], style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True)