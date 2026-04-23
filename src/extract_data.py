"""
Extraction module for the EV Market Pipeline.
Fetches raw vehicle data from external APIs and stages it in the data/ directory.
"""
import requests
import json
import os

def fetch_and_save_car_data():
    # NHTSA API endpoint for Tesla models (placeholder for full market data integration)
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/tesla?format=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        file_path = os.path.join("data", "raw_ev_data.json")
        
        # Ensure target directory exists before writing
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
            
        print(f"[INFO] Successfully extracted data to {file_path}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return None

if __name__ == "__main__":
    fetch_and_save_car_data()