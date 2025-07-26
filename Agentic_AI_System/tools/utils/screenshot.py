import asyncio
import os
from pyppeteer import launch
from core.logger import log

async def _capture(url: str, path: str) -> None:
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 800})
    await page.goto(url)
    await page.screenshot({'path': path, 'fullPage': True})
    await browser.close()

def capture(url: str, path: str) -> None:
    """Capture a screenshot from the given URL."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        asyncio.get_event_loop().run_until_complete(_capture(url, path))
        log.info(f"Screenshot gespeichert unter {path}")
    except Exception as e:
        log.error(f"Screenshot fehlgeschlagen: {e}")
        raise
