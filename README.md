# Australian EV Market Data Pipeline

This is a personal project I put together to track electric vehicle availability and specs in the Australian market. It's an end-to-end ETL pipeline that pulls live data from APIs, cleans it up, and serves it through an interactive dashboard.

## How it Works
The project is built around a "fail-safe" extraction logic. Since third-party APIs can be unreliable or hit rate limits, I built a fallback mechanism:

1. **Extraction:** The script first tries to get deep specifications (drivetrain, efficiency, etc.) from API Ninjas. If that fails or returns an error, it automatically switches to the public NHTSA database to pull the latest models so the pipeline never breaks.
2. **Transformation:** Using Pandas, the raw JSON data is cleaned, column names are standardized, and data types are corrected.
3. **Storage:** The final cleaned dataset is loaded into a local SQLite database (`ev_market.db`).
4. **Dashboard:** A Streamlit app reads from the database to show market distribution, drivetrain splits, and efficiency comparisons using Plotly.

## Project Structure
* `extract_data.py`: Handles the multi-source API logic and saves raw JSON.
* `transform_data.py`: Cleans the raw data and prepares it for the database.
* `load_data.py`: Ingests the cleaned CSV into SQLite.
* `app.py`: The dashboard interface.

## Local Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/AthulJkmr/aus-ev-market-pipeline.git
   cd aus-ev-market-pipeline
   ```

2. **Set up the environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **Add your API Key:**
   Create a `.env` file in the root directory:
   ```text
   API_NINJAS_KEY=your_actual_key_here
   ```

4. **Run the pipeline:**
   ```bash
   python src/extract_data.py
   python src/transform_data.py
   python src/load_data.py
   ```

5. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

## Tech Used
* Python (Requests, Pandas, SQLite3)
* Streamlit
* Plotly Express
* Python-dotenv