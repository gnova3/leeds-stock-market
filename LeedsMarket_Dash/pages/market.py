import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import random
import pandas as pd
from utils.constants import STOCK_LIST, INITIAL_CASH
from utils.simulation import generate_news_event
from utils.database import log_trade, log_chart_view,log_price_evolution
import plotly.graph_objs as go


dash.register_page(__name__, path="/stockmarket")

initial_prices = {stock: 100 + random.uniform(-5, 5) for stock in STOCK_LIST}
portfolio = {stock: 0 for stock in STOCK_LIST}
cash = INITIAL_CASH

layout = dbc.Container([
    #html.H2("Leeds stock market", className="text-center my-4"),

    #html.H4("Market News", className="mt-4"),
    html.Div([
        html.Div(id="news-feed", className="news-ticker-inner")
    ], className="news-ticker my-4", style={
        "width": "80%",
        "margin": "0 auto",
        "overflow": "hidden",
        "whiteSpace": "nowrap",
        "border": "1px solid #ccc",
        "backgroundColor": "#f9f9f9",
        "padding": "8px",
        "fontSize": "16px"
    }),
    dcc.Interval(id="news-update-interval", interval=5000, n_intervals=0),

    # First row: Current Prices and Chart
    dbc.Row([
        dbc.Col([
            html.H4("Current stock prices", className="text-center"),
            html.Div(id="price-table", className="mb-3"),
            dcc.Interval(id="price-update-interval", interval=1000, n_intervals=0)
        ], width=7),

        dbc.Col([
            html.H4("Stock price chart", className="text-center"),
            html.Div([
                dcc.Dropdown(
                    id="chart-stock-select",
                    options=[{"label": s, "value": s} for s in STOCK_LIST],
                    placeholder="Select a stock to view chart",
                    style={"width": "60%", "margin": "0 auto", "marginBottom": "10px"}
                )
            ]),
            dcc.Graph(id="price-chart")
        ], width=5)
    ], className="my-4"),

    # Second row: Trade and Portfolio
    dbc.Row([
        dbc.Col([
            html.H4("Trade", className="text-center"),
            html.Div([
                dcc.Dropdown(
                    id="stock-select",
                    options=[{"label": s, "value": s} for s in STOCK_LIST],
                    placeholder="Select a stock",
                    style={"width": "60%", "margin": "0 auto", "marginBottom": "10px"}
                ),
                dcc.Input(id="quantity", type="number", placeholder="Quantity", min=1,
                          style={"width": "60%", "margin": "0 auto", "display": "block", "marginBottom": "10px"}),
                html.Div([
                    dbc.Button("Buy", id="buy-button", color="success", className="me-2"),
                    dbc.Button("Sell", id="sell-button", color="danger")
                ], className="text-center"),
                html.Div(id="trade-feedback", className="mt-2 text-center", style={"color": "blue"})
            ])
        ], width=5),

        dbc.Col([
            html.H4("Portfolio overview", className="text-center"),
            html.Div(id="portfolio-display", className="my-4"),
        ], width=7)
    ], className="my-4"),

    dcc.Store(id="price-history", data={s: [] for s in STOCK_LIST}),

    # Hidden data stores
    dcc.Store(id="user-id", storage_type="session"),
    dcc.Store(id="price-store", data=initial_prices),
    dcc.Store(id="portfolio-store", data=portfolio),
    dcc.Store(id="cash-store", data=cash),
    dcc.Store(id="news-store", data=[])
], fluid=True)


@dash.callback(
    Output("price-store", "data"),
    Output("price-table", "children"),
    Output("price-history", "data"),
    Input("price-update-interval", "n_intervals"),
    State("price-store", "data"),
    State("price-history", "data")
)
def update_prices(n, prices, history):
    updated_prices = {}
    rows = []
    for stock, price in prices.items():
        delta = random.uniform(-1, 1)
        new_price = round(price * (1 + delta / 100), 2)
        updated_prices[stock] = new_price
        arrow = "▲" if new_price > price else ("▼" if new_price < price else "")
        color = "green" if new_price > price else ("red" if new_price < price else "black")
        rows.append(html.Tr([
            html.Td(stock, style={"maxWidth": "140px", "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"}),
            html.Td(f"€{new_price:.2f}", style={"textAlign": "center"}),
            html.Td(arrow, style={"color": color, "fontWeight": "bold", "textAlign": "center"})
        ]))
        history[stock].append(new_price)
    log_price_evolution(updated_prices)
    table = dbc.Table([
        html.Thead(html.Tr([
            html.Th("Stock"),
            html.Th("Price", style={"textAlign": "center"}),
            html.Th("Δ", style={"textAlign": "center"})
        ]))
    ] + [html.Tbody(rows)], bordered=True)
    return updated_prices, table, history


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
    State("user-id", "data"), 
    prevent_initial_call=True
)
def process_trade(buy_clicks, sell_clicks, stock, qty, prices, port, cash, user_id):
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

    if action in ["buy-button", "sell-button"] and "Insufficient" not in feedback and "Not enough" not in feedback:
        log_trade(
            user_id=dash.callback_context.states["user-id.data"],
            action="buy" if action == "buy-button" else "sell",
            stock=stock,
            quantity=qty,
            price=price,
            total=total
        )
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
            rows.append(html.Tr([
                html.Td(stock),
                html.Td(qty, style={"textAlign": "center"}),
                html.Td(f"€{value:.2f}", style={"textAlign": "center"})
            ]))
    table = dbc.Table(
        [html.Thead(html.Tr([
            html.Th("Stock"),
            html.Th("Quantity", style={"textAlign": "center"}),
            html.Th("Value", style={"textAlign": "center"})
        ]))] +
        [html.Tbody(rows)] +
        [html.Tbody([
            html.Tr([
                html.Td("Cash"),
                html.Td("-", style={"textAlign": "center"}),
                html.Td(f"€{cash:.2f}", style={"textAlign": "center"})
            ]),
            html.Tr([
                html.Td("Total"),
                html.Td("-", style={"textAlign": "center"}),
                html.Td(f"€{total_value:.2f}", style={"textAlign": "center"})
            ])
        ])],
        bordered=True
    )
    return table


@dash.callback(
    Output("news-feed", "children"),
    Input("news-update-interval", "n_intervals")
)
def update_news(n):
    headline = generate_news_event(n)
    return html.Div(f"🗞️ {headline}", style={
        "display": "inline-block",
        "animation": "ticker-scroll 20s linear infinite",
        "paddingLeft": "100%",
        "fontSize": "30px"
    })
import dash


@dash.callback(
    Output("price-chart", "figure"),
    Input("price-history", "data"),
    Input("chart-stock-select", "value"),
    State("user-id", "data")
)
def update_chart(price_history, selected_stock, user_id):
    if selected_stock and user_id:
        log_chart_view(user_id, selected_stock)

    if not selected_stock or selected_stock not in price_history:
        return go.Figure()

    data = price_history[selected_stock]
    fig = go.Figure(data=go.Scatter(
        y=data,
        mode='lines+markers',
        line=dict(color="blue"),
        name=selected_stock
    ))
    fig.update_layout(
        title=f"Price History for {selected_stock}",
        xaxis_title="Time (ticks)",
        yaxis_title="Price (€)",
        margin=dict(l=40, r=20, t=40, b=30),
        height=300
    )
    return fig
# Add ticker-scroll animation CSS
from dash import html as _html
dash.get_app().index_string += """
<style>
@keyframes ticker-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}
</style>
"""