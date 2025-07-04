import asyncio
import requests
import urllib.robotparser
from playwright.async_api import async_playwright, TimeoutError
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote_plus

# DuckDuckGo’s HTML-only search endpoint
DDG_HTML = "https://duckduckgo.com/html?q="
HEADLESS = False  # Set True to hide the browser

async def search_and_scrape(query: str, max_results: int = 5) -> list[str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()

        # 1) Run the DuckDuckGo HTML search
        await page.goto(DDG_HTML + query.replace(" ", "+"))
        await page.wait_for_load_state("networkidle")
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # 2) Extract *all* the <a class="result__a"> anchors
        anchors = soup.find_all("a", class_="result__a")
        if not anchors:
            # fallback for some DDG variants
            bodies = soup.find_all("div", class_="result__body")
            anchors = [b.find("a", class_="result__a") for b in bodies]
            anchors = [a for a in anchors if a]

        results = []
        checked = 0  # how many anchors we've considered

        # 3) Loop until we've got `max_results` good snippets or run out
        for a in anchors:
            if len(results) >= max_results:
                break

            href = a.get("href") or ""
            # Decode DuckDuckGo’s redirect wrapper if needed
            parsed = urlparse(href)
            if parsed.path == "/l/":
                raw = parse_qs(parsed.query).get("uddg", [""])[0]
                href = unquote_plus(raw)

            # Only absolute HTTP(s) URLs
            if not href.startswith(("http://", "https://")):
                continue

            checked += 1
            print(f"\n[{checked}] Considering: {href}")

            # robots.txt check
            rp = urllib.robotparser.RobotFileParser()
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp.set_url(robots_url)
            try:
                rp.read()
                if not rp.can_fetch("*", href):
                    print(f"  ⛔ Disallowed by robots.txt, skipping")
                    continue
                else:
                    print("  ✅ Allowed by robots.txt")
            except Exception:
                print("  ⚠️ robots.txt unavailable, proceeding")

            # Try scraping with Playwright
            print("  → Scraping with Playwright...")
            try:
                await page.goto(href, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                page_html = await page.content()
            except TimeoutError:
                print("    ⏱ Timeout, falling back to requests")
                try:
                    resp = requests.get(href, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                    page_html = resp.text
                except Exception as e:
                    print(f"    ❌ requests fallback failed: {e}")
                    continue
            except Exception as e:
                print(f"    ❌ Playwright failed: {e}")
                continue

            # Clean and extract text
            soup2 = BeautifulSoup(page_html, "html.parser")
            for tag in soup2(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = soup2.get_text(separator=" ", strip=True)

            # Skip if it's just a “JavaScript disabled” notice
            if "javascript is disabled" in text.lower():
                print("    ⚠️ JS-disabled page, skipping")
                continue

            # Good snippet!
            print("    ✔️ Scrape successful")
            results.append(text[:5000])

        await browser.close()
        return results

def get_web_results(query: str) -> list[str]:
    return asyncio.run(search_and_scrape(query))

if __name__ == "__main__":
    q = input("Search for: ")
    snippets = get_web_results(q)
    for idx, snip in enumerate(snippets, 1):
         print(f"\n--- Result {idx} ---\n{snip[:5000]}...\n")
