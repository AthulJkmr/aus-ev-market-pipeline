import pandas as pd
import json
import os

def clean_ev_data():
    input_path = os.path.join("data", "raw_ev_data.json")
    output_path = os.path.join("output", "clean_ev_models.csv")
    
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"Error: Staging file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as file:
        payload = json.load(file)
        
    source = payload.get("source")
    raw_data = payload.get("data", [])
    
    if not raw_data:
        print("Warning: Source payload empty. Aborting transformation.")
        return
        
    df = pd.DataFrame(raw_data)
    
    if source == "api_ninjas":
        target_columns = ["make", "model", "class", "drive", "transmission", "cylinders", "displacement", "year", "city_mpg", "highway_mpg", "combination_mpg"]
        available_columns = [col for col in target_columns if col in df.columns]
        df = df[available_columns].copy()
        
        df["make"] = df["make"].str.capitalize()
        df["model"] = df["model"].str.title()
        if "class" in df.columns: df["class"] = df["class"].str.title()
        if "transmission" in df.columns: df["transmission"] = df["transmission"].str.upper()
            
        df.rename(columns={
            "make": "Manufacturer",
            "model": "Model",
            "class": "Vehicle_Class",
            "drive": "Drivetrain",
            "transmission": "Transmission",
            "cylinders": "Cylinders",
            "displacement": "Engine_Liters",
            "year": "Model_Year",
            "city_mpg": "City_MPGe",
            "highway_mpg": "Highway_MPGe",
            "combination_mpg": "Combined_MPGe"
        }, inplace=True)
        
    else:
        df = df[["Make_Name", "Model_Name"]].copy()
        df.rename(columns={"Make_Name": "Manufacturer", "Model_Name": "Model"}, inplace=True)
        df["Manufacturer"] = df["Manufacturer"].str.capitalize()
        df["Model"] = df["Model"].str.title()
    
    df.drop_duplicates(subset=["Manufacturer", "Model"], inplace=True)
    df.sort_values(by=["Manufacturer", "Model"], inplace=True)
    
    df.to_csv(output_path, index=False)
    print(f"Transformation complete. Mapped {len(df)} records to {output_path}")

if __name__ == "__main__":
    clean_ev_data()