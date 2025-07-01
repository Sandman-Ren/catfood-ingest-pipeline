# Implementation Notes: Catfood Ingest Pipeline

## Project Overview
This project ingests, normalizes, and stores ingredient data for cat food products from Open Pet Food Facts (OFF) and the Mjamjam brand website. The data is stored in a PostgreSQL database and exported in user-friendly formats (CSV, HTML, JSON).

## Key Features & Steps
- **Data Sources:**
  - OFF API (fetch_off.py)
  - Mjamjam website (scrape_mjamjam.py, using Playwright)
- **Normalization:**
  - Ingredient lists are split, cleaned, and mapped to canonical English terms (normalise.py)
- **Database:**
  - PostgreSQL, managed via SQLAlchemy ORM (models.py)
  - Docker Compose setup for easy local database provisioning
- **Pipeline:**
  - `pipeline.py` orchestrates fetching, scraping, normalization, and database upserts
  - After processing, results are exported to CSV, HTML, and JSON in the `output/` directory
- **Logging:**
  - Central logger logs to both stdout and daily-rotated log files (logging_config.py)
- **User Experience:**
  - Designed for non-developers: outputs are readable and easy to open in Excel, browser, or text editor

## Notable Implementation Details
- **Playwright Scraping:**
  - Each category listing is scraped in parallel using a new Playwright page per task (to avoid navigation conflicts)
  - Product details are scraped sequentially
- **Normalization Issues:**
  - Some numbers and unexpected tokens (e.g., "1", "2", "hadi") may appear in the normalized ingredients due to limitations in the current parsing logic
  - Improvements suggested: filter out standalone numbers, expand canonical mapping, and clean up input further
- **Exports:**
  - After running the pipeline, users find results in `output/<brand>_products.csv`, `.html`, and `.json`
- **.gitignore:**
  - Excludes virtual environments, logs, output files, and other common artifacts

## Setup & Usage
1. Install dependencies in a virtual environment (`.venv`)
2. Start PostgreSQL via Docker Compose (`docker compose up -d`)
3. Run the pipeline: `python pipeline.py "Mjamjam"`
4. View results in the `output/` directory

## Next Steps / Improvements
- Refine normalization to filter out numbers and non-ingredient tokens
- Add more ingredient mappings to `normalise.py`
- Optionally, parallelize product detail scraping for further speedup
- Add more user-friendly error messages and documentation

---
_Last updated: July 1, 2025_
