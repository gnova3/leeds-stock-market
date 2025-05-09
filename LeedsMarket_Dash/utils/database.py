#utils/constants.py
import sqlite3
from datetime import datetime

DB_NAME = "experiment_data.db"

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            timestamp TEXT,
            user_agent TEXT,
            ip_address TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS demographics (
            user_id TEXT,
            age TEXT,
            gender TEXT,
            education TEXT,
            income TEXT,
            country TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            user_id TEXT,
            timestamp TEXT,
            action TEXT,
            stock TEXT,
            quantity INTEGER,
            price REAL,
            total REAL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS price_evolution (
            timestamp TEXT,
            stock TEXT,
            price REAL
        )
        """)
        conn.commit()


# Log price evolution for a snapshot of prices (dict: stock->price)
def log_price_evolution(prices):
    now = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        for stock, price in prices.items():
            c.execute("""
                INSERT INTO price_evolution (timestamp, stock, price)
                VALUES (?, ?, ?)
            """, (now, stock, price))
        conn.commit()

def insert_user(user_id, user_agent, ip_address):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, timestamp, user_agent, ip_address)
            VALUES (?, ?, ?, ?)
        """, (user_id, datetime.utcnow().isoformat(), user_agent, ip_address))
        conn.commit()

def insert_demographics(user_id, age, gender, education, income, country):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO demographics (user_id, age, gender, education, income, country)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, age, gender, education, income, country))
        conn.commit()


def log_trade(user_id, action, stock, quantity, price, total):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO trades (user_id, timestamp, action, stock, quantity, price, total)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, datetime.utcnow().isoformat(), action, stock, quantity, price, total))
        conn.commit()

def log_chart_view(user_id, stock):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS chart_views (
                user_id TEXT,
                timestamp TEXT,
                stock TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        c.execute("""
            INSERT INTO chart_views (user_id, timestamp, stock)
            VALUES (?, ?, ?)
        """, (user_id, datetime.utcnow().isoformat(), stock))
        conn.commit()