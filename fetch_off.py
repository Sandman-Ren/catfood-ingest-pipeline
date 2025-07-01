"""Get all cat-food products for a given brand from Open Pet Food Facts.
Example:  python fetch_off.py "Mjamjam"
"""

import requests, urllib.parse as up
from typing import Iterator, Any
from pydantic import BaseModel
from logging_config import logger

BASE = "https://world.openpetfoodfacts.org"

class Product(BaseModel):
    barcode: str
    brand: str | None
    name: str | None
    ingredients_text: str | None
    nutrient_levels: dict[str, Any] | None

def iter_search(brand: str, page_size: int = 100) -> Iterator[Product]:
    logger.info(f"Fetching OFF products for brand: {brand}")
    page = 1
    encoded = up.quote_plus(brand)
    while True:
        url = (f"{BASE}/api/v2/search?"
               f"brand={encoded}&page_size={page_size}&page={page}")
        logger.debug(f"Requesting URL: {url}")
        data = requests.get(url, timeout=30).json()
        for p in data.get("products", []):
            logger.debug(f"Processing product: {p.get('product_name') or p.get('generic_name')}")
            yield Product.model_validate({
                "barcode": p.get("code"),
                "brand": (p.get("brands") or "").split(",")[0].strip(),
                "name": p.get("generic_name") or p.get("product_name"),
                "ingredients_text": p.get("ingredients_text"),
                "nutrient_levels": p.get("nutrient_levels"),
            })
        if page >= data.get("page_count", 0):
            logger.info(f"Completed fetching all pages for brand: {brand}")
            break
        page += 1

if __name__ == "__main__":
    import sys, pandas as pd
    brand = sys.argv[1] if len(sys.argv) > 1 else "Mjamjam"
    logger.info(f"Exporting OFF data for brand: {brand}")
    rows = [p.model_dump() for p in iter_search(brand)]
    pd.DataFrame(rows).to_csv(f"{brand}_off.csv", index=False)
    logger.info(f"Saved {len(rows)} rows → {brand}_off.csv")
    print(f"Saved {len(rows)} rows → {brand}_off.csv")
