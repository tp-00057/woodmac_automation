import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import time


@asynccontextmanager
async def get_playwright_page(fullscreen=False):
    """
    Returns a new Page object directly.
    Handles the lifecycle of Browser, Context, and Page.
    """
    async with async_playwright() as p:
        launch_args = ["--start-maximized"] if fullscreen else []

        browser = await p.chromium.launch(
            channel="msedge",
            headless=False,
            args=launch_args
        )

        # no_viewport=True is necessary for the maximized window to fill correctly
        context = await browser.new_context(no_viewport=fullscreen)
        page = await context.new_page()

        try:
            yield page
        finally:
            # Closing the context automatically closes all pages within it
            await context.close()
            await browser.close()


# --- Reusable Business Logic ---

async def click_four_divs(page, selectors):
    for selector in selectors:
        await page.wait_for_selector(selector)
        await page.click(selector)
        await asyncio.sleep(2)
        print(f"Successfully clicked: {selector}")


# --- Execution ---

async def main():
    target_selectors = [
        "#pageHeader > div > div > div.header__container > div.header__left > nav > div > div:nth-child(1)",
        "#pageHeader > div > div > div.header__container > div.header__left > nav > div > div:nth-child(2)",
        "#pageHeader > div > div > div.header__container > div.header__left > nav > div > div:nth-child(3)"
       ]

    # One-liner to get a ready-to-use page
    async with get_playwright_page(fullscreen=False) as page:
        await page.goto("https://www.cnn.com/")
        await click_four_divs(page, target_selectors)
        time.sleep(5)
        # You can perform any other actions here before the block ends
        #content = await page.content()
        print("Task completed.")


if __name__ == "__main__":
    asyncio.run(main())