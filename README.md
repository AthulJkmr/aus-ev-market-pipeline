# Australian EV Market Data Pipeline

I built this project to get a better handle on the electric vehicle market in Australia. It’s an end-to-end ETL (Extract, Transform, Load) pipeline that pulls data from external APIs, cleans it up, and displays it in an interactive dashboard.

## The Goal
The idea was to create a resilient system that could handle real-world API issues. If the primary data source (API Ninjas) fails or hits a rate limit, the script automatically switches over to a public NHTSA backup so the dashboard stays updated.

## Project Structure

* **Extraction:** Hits the API Ninjas Cars endpoint for deep specs. If it gets a 400 error, it triggers a fallback sequence to pull model names from the NHTSA database.
* **Transformation:** Uses Pandas to normalize different API schemas, clean up string formatting (capitalization, etc.), and handle missing values.
* **Loading:** Ingests the final dataset into a local SQLite database (`ev_market.db`) for easy querying.
* **Dashboard:** A Streamlit app that lets you filter by manufacturer and drivetrain to see market distribution and efficiency stats via Plotly.

## Getting Started

### 1. Setup
Clone the repo and set up a fresh virtual environment:

```bash
git clone [https://github.com/AthulJkmr/aus-ev-market-pipeline.git](https://github.com/AthulJkmr/aus-ev-market-pipeline.git)
cd aus-ev-market-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt