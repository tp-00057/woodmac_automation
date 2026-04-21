import asyncio
from utils.browser_utils import get_page  # Import your utility

async def run_extraction():
    async with get_page(fullscreen=True) as page:
        await page.goto("https://www.costco.com")
        print(f"Working on: {await page.title()}")

if __name__ == "__main__":
    asyncio.run(run_extraction())