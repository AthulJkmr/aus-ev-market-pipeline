import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

def fetch_ev_data():
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "raw_ev_data.json")
    all_vehicles = []
    
    api_key = os.getenv("API_NINJAS_KEY")
    if api_key:
        print("Initiating primary extraction sequence (API Ninjas)...")
        headers = {'X-Api-Key': api_key}
        target_vehicles = {
            "tesla": ["model 3", "model y"],
            "hyundai": ["ioniq 5", "kona"],
            "kia": ["ev6", "niro"]
        }
        
        for brand, models in target_vehicles.items():
            for model in models:
                params = {'make': brand, 'model': model}
                try:
                    response = requests.get("https://api.api-ninjas.com/v1/cars", headers=headers, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            all_vehicles.extend(data)
                    time.sleep(1)
                except requests.exceptions.RequestException:
                    pass
                    
    if len(all_vehicles) > 0:
        print(f"Primary extraction successful. Staged {len(all_vehicles)} records.")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"source": "api_ninjas", "data": all_vehicles}, f, indent=4)
        return

    print("Warning: Primary API failed or returned 400 Bad Request.")
    print("Initiating automated fallback to public NHTSA database...")
    
    fallback_brands = ["tesla", "hyundai", "kia", "polestar", "toyota"]
    for brand in fallback_brands:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{brand}?format=json"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                results = res.json().get("Results", [])
                all_vehicles.extend(results[:15])
        except Exception as e:
            print(f"Error: Fallback failed for {brand}: {e}")
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"source": "nhtsa", "data": all_vehicles}, f, indent=4)
        
    print(f"Fallback extraction complete. Staged {len(all_vehicles)} records to {file_path}")

if __name__ == "__main__":
    fetch_ev_data()