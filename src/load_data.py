import pandas as pd
import sqlite3
import os

def load_to_database():
    csv_path = os.path.join("output", "clean_ev_models.csv")
    db_path = os.path.join("output", "ev_market.db")
    
    if not os.path.exists(csv_path):
        print(f"Error: Staging CSV not found: {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
        
        with sqlite3.connect(db_path) as conn:
            df.to_sql("vehicles", conn, if_exists="replace", index=False)
            
        print(f"Successfully loaded {len(df)} records into {db_path}")
        
    except Exception as e:
        print(f"Error: Database load failed: {e}")

if __name__ == "__main__":
    load_to_database()