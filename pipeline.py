"""Run:   python pipeline.py "Mjamjam"
 1. pulls OFF data
 2. scrapes brand website
 3. canonicalises ingredient lists
 4. writes / updates into Postgres
"""

import json, subprocess, tempfile, sys, asyncio
import pandas as pd
from pathlib import Path

from fetch_off import iter_search
from normalise import canonicalise
from models import get_session, Brand, Product
from logging_config import logger

def upsert(session, brand_name, title, raw, canonical, barcode=None, source="scraper"):
    logger.debug(f"Upserting product: brand={brand_name}, title={title}, barcode={barcode}, source={source}")
    brand = session.query(Brand).filter_by(name=brand_name).first()
    if not brand:
        logger.info(f"Creating new brand: {brand_name}")
        brand = Brand(name=brand_name)
        session.add(brand)
        session.flush()
    prod = session.query(Product).filter_by(title=title, brand=brand).first()
    if not prod:
        logger.info(f"Creating new product: {title} (brand={brand_name})")
        prod = Product(brand=brand, title=title)
        session.add(prod)
    prod.barcode = barcode or ""
    prod.raw_ingredients = raw
    prod.ingredients = canonical
    prod.source = source

def run_off(brand, session):
    logger.info(f"Fetching OFF data for brand: {brand}")
    for p in iter_search(brand):
        if not p.ingredients_text:
            logger.debug(f"Skipping product with no ingredients: {p.name}")
            continue
        can = canonicalise(p.ingredients_text)
        upsert(session, p.brand or brand, p.name or "N/A",
               p.ingredients_text, can, barcode=p.barcode, source="OFF")
    logger.info("OFF data fetch complete.")

async def run_scraper(session):
    logger.info("Running Mjamjam scraper...")
    proc = subprocess.Popen(
        [sys.executable, "scrape_mjamjam.py"],
        stdout=subprocess.PIPE,
        text=True
    )
    for line in proc.stdout or []:
        data = json.loads(line)
        if not data.get("ingredients"):
            logger.debug(f"Skipping scraped product with no ingredients: {data.get('title')}")
            continue
        can = canonicalise(data["ingredients"])
        upsert(session, "Mjamjam", data["title"], data["ingredients"], can)
    proc.wait()
    logger.info("Mjamjam scraping complete.")

def export_results(session, brand):
    logger.info(f"Exporting results for brand: {brand}")
    products = (
        session.query(Product)
        .join(Brand)
        .filter(Brand.name == brand)
        .all()
    )
    if not products:
        logger.warning(f"No products found for brand: {brand}")
        print(f"No products found for brand: {brand}")
        return
    rows = [
        {
            "title": p.title,
            "raw_ingredients": p.raw_ingredients,
            "ingredients": p.ingredients,
            "barcode": p.barcode,
            "source": p.source,
        }
        for p in products
    ]
    df = pd.DataFrame(rows)
    outdir = Path("output")
    outdir.mkdir(exist_ok=True)
    csv_path = outdir / f"{brand}_products.csv"
    html_path = outdir / f"{brand}_products.html"
    json_path = outdir / f"{brand}_products.json"
    df.to_csv(csv_path, index=False)
    df.to_html(html_path, index=False)
    df.to_json(json_path, orient="records", force_ascii=False, indent=2)
    logger.info(f"Exported to: {csv_path}, {html_path}, {json_path}")
    print(f"\nResults exported to:\n- {csv_path}\n- {html_path}\n- {json_path}")

def main(brand):
    logger.info(f"Starting pipeline for brand: {brand}")
    session = get_session()
    run_off(brand, session)
    asyncio.run(run_scraper(session))
    session.commit()
    logger.info("✓ pipeline finished")
    print("✓ pipeline finished")
    export_results(session, brand)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Mjamjam")
