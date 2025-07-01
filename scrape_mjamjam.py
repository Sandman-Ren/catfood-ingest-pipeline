"""Usage:  python scrape_mjamjam.py > mjamjam_raw.jsonl"""

import asyncio, json
from playwright.async_api import async_playwright

CAT_BASE = "https://www.mjamjam-petfood.de/katzen"

# CSS selectors are stable as of 30 Jun 2025 —
SEL_PRODUCT = "a.product--title"
SEL_ING = "div.product--properties strong:has-text('Zusammensetzung') + p"

slug_cats = [
    "leckere-mahlzeiten", "purer-fleischgenuss", "soßenschmaus", "snackbar",
    "insekt", "mixpakete", "kitten", "purer-filetgenuss", "chicks-friends"
]

async def scrape_listing(browser, slug):
    page = await browser.new_page()
    await page.goto(f"{CAT_BASE}/{slug}", timeout=60000)
    links = [await a.get_attribute("href") for a in await page.query_selector_all(SEL_PRODUCT)]
    await page.close()
    return links

async def scrape_product(page, url):
    await page.goto(url, timeout=60000)
    title = await page.title()
    ing_el = await page.query_selector(SEL_ING)
    ing = await ing_el.inner_text() if ing_el else None
    return {"url": url, "title": title, "ingredients": ing}

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        # Use a new page per listing
        tasks = [scrape_listing(browser, slug) for slug in slug_cats]
        listings = await asyncio.gather(*tasks)
        product_urls = sorted(set(url for lst in listings for url in lst))

        results = []
        page = await browser.new_page()
        for url in product_urls:
            try:
                results.append(await scrape_product(page, url))
            except Exception as e:
                print(f"# Error {url}: {e}", flush=True)
        await page.close()
        await browser.close()

    print("\n".join(json.dumps(r, ensure_ascii=False) for r in results))

if __name__ == "__main__":
    asyncio.run(main())
