from playwright.sync_api import sync_playwright, TimeoutError
import requests
import urllib.robotparser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote_plus

DDG_HTML = "https://duckduckgo.com/html?q="
HEADLESS = False 

def search_and_scrape(query: str, max_results: int = 5) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto(DDG_HTML + query.replace(" ", "+"))
        page.wait_for_load_state("networkidle")
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.find_all("a", class_="result__a")
        if not anchors:
            # fallback for some DDG variants
            bodies = soup.find_all("div", class_="result__body")
            anchors = [b.find("a", class_="result__a") for b in bodies]
            anchors = [a for a in anchors if a]
        results = []
        for a in anchors:
            if len(results) >= max_results:
                break
            href = a.get("href") or ""
            parsed = urlparse(href)
            if parsed.path == "/l/":
                raw = parse_qs(parsed.query).get("uddg", [""])[0]
                href = unquote_plus(raw)
            if not href.startswith(("http://", "https://")):
                continue
            rp = urllib.robotparser.RobotFileParser()
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp.set_url(robots_url)
            try:
                rp.read()
                if not rp.can_fetch("*", href):
                    continue
            except Exception:
                pass
            try:
                page.goto(href, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                page_html = page.content()
            except TimeoutError:
                try:
                    resp = requests.get(href, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                    page_html = resp.text
                except Exception:
                    continue
            except Exception:
                continue
            soup2 = BeautifulSoup(page_html, "html.parser")
            for tag in soup2(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = soup2.get_text(separator=" ", strip=True)
            if "javascript is disabled" in text.lower():
                continue
            results.append(text[:5000])
        browser.close()
        return results

def get_web_results(query: str) -> list[str]:
    return search_and_scrape(query)

if __name__ == "__main__":
    q = input("Search for: ")
    snippets = get_web_results(q)
    for idx, snip in enumerate(snippets, 1):
         print(f"\n--- Result {idx} ---\n{snip[:5000]}...\n")
