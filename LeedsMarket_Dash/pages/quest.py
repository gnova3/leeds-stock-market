#pages/quest.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from utils.database import insert_demographics

dash.register_page(__name__, path="/questionnaire")

layout = html.Div([
    html.H2("Participant Questionnaire"),
    dbc.Form([
        dbc.Label("1. What is your age group?"),
        dcc.Dropdown(
            id="age-dropdown",
            options=[
                {"label": "Under 20", "value": "<20"},
                {"label": "20-29", "value": "20-29"},
                {"label": "30-39", "value": "30-39"},
                {"label": "40-49", "value": "40-49"},
                {"label": "50 and above", "value": "50+"}
            ],
            placeholder="Select your age group"
        ),
        dbc.Label("2. What is your gender?"),
        dcc.Dropdown(
            id="gender-dropdown",
            options=[
                {"label": "Male", "value": "Male"},
                {"label": "Female", "value": "Female"},
                {"label": "Other / Prefer not to say", "value": "Other"}
            ],
            placeholder="Select your gender"
        ),
        dbc.Label("3. What is your highest education level?"),
        dcc.Dropdown(
            id="education-dropdown",
            options=[
                {"label": "High School", "value": "High School"},
                {"label": "Bachelor's Degree", "value": "Bachelors"},
                {"label": "Master's Degree", "value": "Masters"},
                {"label": "PhD or higher", "value": "PhD"},
                {"label": "Other", "value": "Other"}
            ],
            placeholder="Select your education level"
        ),
        dbc.Label("4. What is your income level?"),
        dcc.Dropdown(
            id="income-dropdown",
            options=[
                {"label": "Low", "value": "Low"},
                {"label": "Medium", "value": "Medium"},
                {"label": "High", "value": "High"}
            ],
            placeholder="Select your income level"
        ),
        dbc.Label("5. In which country do you currently live?"),
        dcc.Input(id="country-input", type="text", placeholder="Enter your country"),
        html.Br(), html.Br(),
        dbc.Button("Submit", id="submit-questionnaire", color="success")
    ]),
    html.Div(id="form-warning", style={"color": "red", "marginTop": "10px"}),
    dcc.Location(id="questionnaire-location")
])

@dash.callback(
    Output("questionnaire-location", "href"),
    Output("form-warning", "children"),
    Input("submit-questionnaire", "n_clicks"),
    State("user-id", "data"),
    State("age-dropdown", "value"),
    State("gender-dropdown", "value"),
    State("education-dropdown", "value"),
    State("income-dropdown", "value"),
    State("country-input", "value"),
    prevent_initial_call=True
)
def submit_form(n_clicks, user_id, age, gender, education, income, country):
    if not all([user_id, age, gender, education, income, country]):
        return None, "Please complete all questions before continuing."
    insert_demographics(user_id, age, gender, education, income, country)
    return "/stockmarket", ""