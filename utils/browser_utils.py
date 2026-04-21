import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright

@asynccontextmanager
async def get_page(fullscreen=False):
    """
    Centralized browser factory for Microsoft Edge.
    """
    async with async_playwright() as p:
        launch_args = ["--start-maximized"] if fullscreen else []
        browser = await p.chromium.launch(
            channel="msedge",
            headless=False,
            args=launch_args
        )
        context = await browser.new_context(no_viewport=fullscreen)
        page = await context.new_page()
        try:
            yield page
        finally:
            await context.close()
            await browser.close()