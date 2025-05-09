#pages/intro.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import uuid
from flask import request

from utils.database import insert_user, create_tables

dash.register_page(__name__, path="/")

create_tables()

layout = dbc.Container([
    html.H2("Informed consent form", className="my-4 text-center"),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("""
You are invited to participate in a research simulation called the *Stock Market Simulation Experiment*, which takes approximately 30 minutes.

During this simulation, you will interact with a virtual stock market environment that includes 10 tradable assets. You will have the ability to buy and sell shares, react to market news, and observe the influence of other simulated participants on stock prices. The purpose of this study is to understand how individuals behave in dynamic market environments.

As with any online activity, there is a small risk of data breach. We have taken precautions to minimise these risks:
1. We do not collect any personally identifiable information.
2. All data is stored securely on servers located at the University of Leeds and is accessible only to the research team.

Participation is voluntary, and you may withdraw at any time. The data collected, including your trading behaviour and decision-making patterns, may be used anonymously in scientific publications or academic presentations.

Thank you for your participation. By checking the box and clicking the “Continue” button below, you indicate that you have read and understood the conditions of participation and agree to take part in this study.
""", className="mb-3"),
            html.Div([
                dbc.Checklist(
                    options=[{"label": "I agree to participate", "value": 1}],
                    id="consent-checkbox",
                    inline=True,
                    className="mb-3"
                ),
                dbc.Button("Continue", id="submit-consent", color="primary", disabled=True, className="mb-4")
            ], className="text-center"),
            dcc.Store(id="consent-submitted", data=False),
            dcc.Location(id="consent-location", refresh=True)
        ], width=6, className="offset-md-3")
    ])
], fluid=True)

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
    State("consent-checkbox", "value"),
    prevent_initial_call=True
)
def submit_consent(n_clicks, consent_value):
    if not consent_value or 1 not in consent_value:
        return dash.no_update, dash.no_update
    user_id = str(uuid.uuid4())
    ua = request.headers.get('User-Agent', 'unknown')
    ip = request.remote_addr or "unknown"
    insert_user(user_id, ua, ip)
    return "/questionnaire", user_id