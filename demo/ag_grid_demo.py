import asyncio
from utils.browser_utils import get_page
from utils.soup_utils import extract_ag_grid_data, export_to_json
from bs4 import BeautifulSoup


async def run_export():
    url = "https://www.ag-grid.com/example/"
    all_rows = set()  # Using a set prevents duplicates from overlapping scrolls

    async with get_page(fullscreen=True) as page:
        await page.goto(url)
        # Wait for the grid to initialize
        await page.wait_for_selector(".ag-center-cols-container")

        # 1. Capture Headers
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        headers = [h.get_text(strip=True) for h in soup.select(".ag-header-cell-text")]

        # 2. Identify the scrollable viewport
        viewport_selector = ".ag-body-viewport"

        # 3. Scroll Loop: Adjust the range for larger datasets
        for i in range(15):
            print(f"Scrolling and capturing step {i + 1}...")

            # Extract rows currently in the DOM
            current_html = await page.content()
            new_rows = extract_ag_grid_data(current_html)
            all_rows.update(new_rows)

            # Scroll down by 600 pixels inside the grid container
            await page.evaluate(f"""
                document.querySelector('{viewport_selector}').scrollBy(0, 600);
            """)

            # Wait for the grid to "paint" new rows (virtualization delay)
            await asyncio.sleep(0.7)

        # 4. Final Export
        export_to_json(all_rows, headers)


if __name__ == "__main__":
    asyncio.run(run_export())