import os

import psycopg2
import time
import requests as request 
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook  

def fetch_and_store():
    print("Starting REAL pipeline...")
    hook = PostgresHook(postgres_conn_id="postgres_default")


    # CONNECT
conn = hook.get_conn()
cur = conn.cursor()

    # CREATE TABLE
cur.execute("""
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id SERIAL PRIMARY KEY,
        name TEXT,
        price_usd FLOAT,
        created_at TIMESTAMP
    );
    """)
conn.commit()

print("Table ready. Fetching crypto data...\n")

    # LOOP
try:
       url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
       response = request.get(url)
       data = response.json()
       
       now = datetime.now()
       for coin in data:
            name = coin["name"]
            price = coin["current_price"]
            
            cur.execute("""
            INSERT INTO crypto_prices (name, price_usd, created_at)
            VALUES (%s, %s, %s);
            """, (name, price, now))
            conn.commit()
       print(f"[{now.strftime('%H:%M:%S')}] Inserted {len(data)} top coins")
except Exception as e:
        print("ERRoR:",e)
        
except KeyboardInterrupt:
        print("\nPipeline stopped by user.")
finally:
        cur.close()
        conn.close()
        print("Task Finished.")