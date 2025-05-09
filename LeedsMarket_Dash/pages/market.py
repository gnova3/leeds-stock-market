#pages/market.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import random
import pandas as pd
from utils.constants import STOCK_LIST, INITIAL_CASH

dash.register_page(__name__, path="/stockmarket")

# Initial dummy stock prices
initial_prices = {stock: 100 + random.uniform(-5, 5) for stock in STOCK_LIST}
portfolio = {stock: 0 for stock in STOCK_LIST}
cash = INITIAL_CASH

layout = html.Div([
    html.H2("Live Stock Market Simulation"),
    dbc.Row([
        dbc.Col([
            html.H4("Current Stock Prices"),
            html.Div(id="price-table"),
            dcc.Interval(id="price-update-interval", interval=1000, n_intervals=0)
        ], width=6),
        dbc.Col([
            html.H4("Trade"),
            dcc.Dropdown(
                id="stock-select",
                options=[{"label": s, "value": s} for s in STOCK_LIST],
                placeholder="Select a stock"
            ),
            dcc.Input(id="quantity", type="number", placeholder="Quantity", min=1),
            dbc.Button("Buy", id="buy-button", color="success", className="me-2"),
            dbc.Button("Sell", id="sell-button", color="danger"),
            html.Div(id="trade-feedback", className="mt-2", style={"color": "blue"}),
            html.Hr(),
            html.H4("Portfolio Overview"),
            html.Div(id="portfolio-display")
        ], width=6),
    ]),
    html.Hr(),
    html.H4("Market News"),
    html.Div(id="news-feed", style={"maxHeight": "200px", "overflowY": "scroll", "border": "1px solid #ccc", "padding": "10px"}),
    dcc.Store(id="user-id", storage_type="session"),
    dcc.Store(id="price-store", data=initial_prices),
    dcc.Store(id="portfolio-store", data=portfolio),
    dcc.Store(id="cash-store", data=cash)
])

@dash.callback(
    Output("price-store", "data"),
    Output("price-table", "children"),
    Input("price-update-interval", "n_intervals"),
    State("price-store", "data")
)
def update_prices(n, prices):
    updated_prices = {}
    rows = []
    for stock, price in prices.items():
        delta = random.uniform(-1, 1)
        new_price = round(price * (1 + delta / 100), 2)
        updated_prices[stock] = new_price
        rows.append(html.Tr([html.Td(stock), html.Td(f"€{new_price:.2f}")]))
    table = dbc.Table([html.Thead(html.Tr([html.Th("Stock"), html.Th("Price")]))] + [html.Tbody(rows)], bordered=True)
    return updated_prices, table

@dash.callback(
    Output("portfolio-store", "data"),
    Output("cash-store", "data"),
    Output("trade-feedback", "children"),
    Input("buy-button", "n_clicks"),
    Input("sell-button", "n_clicks"),
    State("stock-select", "value"),
    State("quantity", "value"),
    State("price-store", "data"),
    State("portfolio-store", "data"),
    State("cash-store", "data"),
    prevent_initial_call=True
)
def process_trade(buy_clicks, sell_clicks, stock, qty, prices, port, cash):
    ctx = dash.callback_context
    if not ctx.triggered or not stock or not qty:
        return port, cash, "Invalid trade input."

    action = ctx.triggered[0]["prop_id"].split(".")[0]
    price = prices.get(stock, 0)
    qty = int(qty)
    total = qty * price

    if action == "buy-button":
        if cash >= total:
            port[stock] += qty
            cash -= total
            feedback = f"Bought {qty} shares of {stock} at €{price:.2f}"
        else:
            feedback = "Insufficient funds."
    elif action == "sell-button":
        if port.get(stock, 0) >= qty:
            port[stock] -= qty
            cash += total
            feedback = f"Sold {qty} shares of {stock} at €{price:.2f}"
        else:
            feedback = "Not enough shares to sell."
    else:
        feedback = "Unknown action."

    return port, cash, feedback

@dash.callback(
    Output("portfolio-display", "children"),
    Input("portfolio-store", "data"),
    Input("cash-store", "data"),
    State("price-store", "data")
)
def update_portfolio_display(port, cash, prices):
    rows = []
    total_value = cash
    for stock, qty in port.items():
        if qty > 0:
            price = prices.get(stock, 0)
            value = qty * price
            total_value += value
            rows.append(html.Tr([html.Td(stock), html.Td(qty), html.Td(f"€{value:.2f}")]))
    table = dbc.Table(
        [html.Thead(html.Tr([html.Th("Stock"), html.Th("Quantity"), html.Th("Value")]))] +
        [html.Tbody(rows)] +
        [html.Tbody([html.Tr([html.Td("Cash"), html.Td("-"), html.Td(f"€{cash:.2f}")]),
                     html.Tr([html.Td("Total"), html.Td("-"), html.Td(f"€{total_value:.2f}")])])],
        bordered=True
    )
    return table
