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