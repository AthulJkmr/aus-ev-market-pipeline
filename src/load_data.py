"""
Load module for the EV Market Pipeline.
Ingests cleaned CSV data into the local SQLite analytics database.
"""
import pandas as pd
import sqlite3
import os

def load_to_database():
    csv_path = os.path.join("output", "clean_ev_models.csv")
    db_path = os.path.join("output", "ev_market.db")
    
    if not os.path.exists(csv_path):
        print(f"[ERROR] Staging CSV not found: {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
        
        # Connect to SQLite DB (creates file if it doesn't exist)
        with sqlite3.connect(db_path) as conn:
            # Upsert strategy: replace for MVP, will migrate to append/merge later
            df.to_sql("vehicles", conn, if_exists="replace", index=False)
            
        print(f"[INFO] Successfully loaded {len(df)} records into {db_path} (Table: vehicles)")
        
    except Exception as e:
        print(f"[ERROR] Database load failed: {e}")

if __name__ == "__main__":
    load_to_database()