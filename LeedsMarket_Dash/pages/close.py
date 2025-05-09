#pages/close.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

dash.register_page(__name__, path="/closing")

layout = html.Div([
    html.H2("Simulation Complete"),
    html.P("Thank you for participating in the Stock Market Simulation."),
    html.Br(),
    html.P("Your session has ended. All your trades and interactions have been recorded."),
    html.P("You may now close this tab or return to the host if part of an organized study."),
    html.Br(),
    dbc.Alert("Final results have been saved successfully.", color="success"),
    html.Hr(),
    html.Footer("© 2025 Choice Modelling Centre — University of Leeds")
])