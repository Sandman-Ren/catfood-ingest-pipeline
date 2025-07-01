# Catfood Ingest Pipeline

> **Disclaimer:** This project was generated entirely by GitHub Copilot, with no human intervention except for providing prompts. All code, documentation, and instructions were produced by Copilot based on user requests.

This project provides a data ingestion pipeline for collecting, normalizing, and storing ingredient data for cat food products from both Open Pet Food Facts (OFF) and the Mjamjam brand website. The pipeline is designed for research, analysis, or integration with other systems, and stores results in a PostgreSQL database.

## Features
- **Fetches cat food product data** from Open Pet Food Facts by brand
- **Scrapes product and ingredient data** from the Mjamjam website using Playwright
- **Normalizes ingredient lists** to canonical English terms
- **Stores and updates data** in a PostgreSQL database using SQLAlchemy ORM
- **Exports results** to CSV, HTML, and JSON for easy viewing and sharing
- **User-friendly output**: Designed for non-developers; results are readable in Excel, browser, or text editor

## Set Up Guide (For Everyone)

Follow these steps to set up and run the project on your own computer. No programming experience is required!

### 1. Install Prerequisites
- **Python**: Download and install Python 3.10 or newer from [python.org](https://www.python.org/downloads/).
- **Docker Desktop**: Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/). This lets you run the database easily.
- **Git (optional)**: If you want to clone the project from GitHub, install Git from [git-scm.com](https://git-scm.com/downloads/).

### 2. Download the Project
- If you have Git, open a terminal and run:
  ```sh
  git clone <repository-url>
  cd catfood_ingest
  ```
- Or, download the project as a ZIP file from GitHub and unzip it. Open a terminal and `cd` into the project folder.

### 3. Set Up the Database
- In your terminal, run:
  ```sh
  docker compose up -d
  ```
- This will start a PostgreSQL database in the background. You only need to do this once, and the database will keep running until you stop it.

### 4. Set Up Python Environment
- In your terminal, run:
  ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- This creates a safe environment for the project and installs all needed packages.

### 5. Install Playwright Browsers
- Still in your terminal, run:
  ```sh
  playwright install
  ```
- This step is required for the web scraping part to work.

### 6. Run the Pipeline
- To collect and process the data, run:
  ```sh
  python pipeline.py "Mjamjam"
  ```
- The program will fetch, scrape, and process the data. When finished, it will create files in the `output/` folder.

### 7. View the Results
- Open the `output/` folder. You will find:
  - `.csv` file: Open in Excel or Google Sheets
  - `.html` file: Open in any web browser
  - `.json` file: Open in a text editor or use for further processing

### 8. (Optional) Stop the Database
- When you are done, you can stop the database with:
  ```sh
  docker compose down
  ```

---

## Project Structure
- `pipeline.py` — Main entry point; runs the full pipeline for a given brand, exports results
- `fetch_off.py` — Fetches product data from OFF API
- `scrape_mjamjam.py` — Scrapes product data from the Mjamjam website
- `normalise.py` — Normalizes ingredient lists to canonical terms
- `models.py` — SQLAlchemy ORM models and DB session setup
- `logging_config.py` — Logging setup for stdout and log files
- `requirements.txt` — Python dependencies
- `docker-compose.yml` — For running PostgreSQL with Docker
- `output/` — Directory for exported CSV, HTML, and JSON files

## Usage Details

- **Fetch OFF data only:**
  ```sh
  python fetch_off.py "Mjamjam"
  ```
  Saves results as CSV.

- **Scrape Mjamjam only:**
  ```sh
  python scrape_mjamjam.py > mjamjam_raw.jsonl
  ```
  Outputs raw JSON lines.

- **Normalize ingredients:**
  See `normalise.py` for canonicalization logic and test via its `__main__`.

- **View/export results:**
  After running the pipeline, open the files in the `output/` directory:
  - `.csv`: Open in Excel or Google Sheets
  - `.html`: Open in any web browser
  - `.json`: Open in a text editor or use for further processing

## Requirements
- Python 3.10+
- PostgreSQL database (can use Docker Compose)
- Playwright (for scraping)
- See `requirements.txt` for all Python dependencies

## Troubleshooting
- If you see database connection errors, ensure PostgreSQL is running and accessible.
- If you see unexpected tokens (like numbers or unknown words) in the ingredients, see `normalise.py` for how to improve normalization.

## License
MIT License
