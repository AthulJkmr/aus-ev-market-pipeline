"""
Transformation module for the EV Market Pipeline.
Cleans raw JSON data, standardizes schema, and outputs a staging CSV.
"""
import pandas as pd
import json
import os

def clean_ev_data():
    input_path = os.path.join("data", "raw_ev_data.json")
    output_path = os.path.join("output", "clean_ev_models.csv")
    
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        
    car_list = raw_data.get("Results", [])
    
    if not car_list:
        print("[WARNING] No vehicle data found in source payload.")
        return
        
    df = pd.DataFrame(car_list)
    
    # Schema mapping
    df = df[["Make_Name", "Model_Name"]].copy()
    df.rename(columns={
        "Make_Name": "Manufacturer",
        "Model_Name": "Model"
    }, inplace=True)
    
    # Deduplicate and sort
    df.drop_duplicates(inplace=True)
    df.sort_values(by=["Manufacturer", "Model"], inplace=True)
    
    df.to_csv(output_path, index=False)
    print(f"[INFO] Data transformation complete. Staged {len(df)} records at {output_path}")

if __name__ == "__main__":
    clean_ev_data()