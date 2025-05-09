#pages/intro.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import uuid
from flask import request

from utils.database import insert_user, create_tables

dash.register_page(__name__, path="/")

create_tables()

layout = html.Div([
    html.H2("Consent Form"),
    dcc.Markdown("""
    Welcome to the stock market simulation study. Please read the consent form below.

    [Consent form content here...]

    By clicking "I Agree", you agree to participate.
    """),
    dbc.Checklist(
        options=[{"label": "I agree to participate", "value": 1}],
        id="consent-checkbox",
        inline=True
    ),
    html.Br(),
    dbc.Button("Continue", id="submit-consent", color="primary", disabled=True),
    dcc.Store(id="consent-submitted", data=False),
    dcc.Location(id="consent-location")
])

@dash.callback(
    Output("submit-consent", "disabled"),
    Input("consent-checkbox", "value")
)
def toggle_button(consent_value):
    return not (consent_value and 1 in consent_value)

@dash.callback(
    Output("consent-location", "href"),
    Output("user-id", "data"),
    Input("submit-consent", "n_clicks"),
    prevent_initial_call=True
)
def submit_consent(n_clicks):
    user_id = str(uuid.uuid4())
    ua = request.headers.get('User-Agent', 'unknown')
    ip = request.remote_addr or "unknown"
    insert_user(user_id, ua, ip)
    return "/questionnaire", user_id