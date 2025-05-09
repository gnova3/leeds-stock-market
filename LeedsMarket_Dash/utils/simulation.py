#utils/simulation.py
import random
from utils.constants import STOCK_LIST

def simulate_price_tick(prices, user_impact=None):
    """
    Simulates the next tick of prices using a stochastic model (GBM-like) 
    and adjusts based on user interactions (optional).

    Parameters:
        prices (dict): current prices for each stock.
        user_impact (dict): optional dictionary with stock: net buy/sell influence.

    Returns:
        dict: updated stock prices
    """
    updated = {}
    for stock in STOCK_LIST:
        p = prices[stock]
        drift = 0.0002
        volatility = 0.01
        noise = random.gauss(0, volatility)
        impact = user_impact.get(stock, 0) * 0.001 if user_impact else 0
        new_price = round(p * (1 + drift + noise + impact), 2)
        updated[stock] = max(new_price, 0.01)
    return updated

def generate_news_event(n):
    """
    Randomly creates a simulated news headline.

    Parameters:
        n (int): news number or tick index for seeding.

    Returns:
        str: news headline
    """
    random.seed(n)
    headlines = [
        "Central bank announces interest rate hike.",
        "Tech giant reports record-breaking earnings.",
        "Unexpected drop in consumer confidence index.",
        "Oil prices surge due to geopolitical tension.",
        "New regulations on financial trading imposed.",
        "Breakthrough in renewable energy technology.",
        "Housing market shows signs of overheating.",
        "Supply chain disruptions affect major retailers.",
        "Investors flock to safe-haven assets amid uncertainty.",
        "Pharma stock soars on positive trial results."
    ]
    return random.choice(headlines)