import asyncio
from utils.browser_utils import get_page
from utils.soup_utils import extract_ag_grid_smart_merge, save_table_to_json


async def main():
    # STEP 1: Identify your pinned column ID (usually 'athlete', 'id', or '0')
    PINNED_COL_ID = "athlete"

    async with get_page(fullscreen=True) as page:
        await page.goto("https://www.ag-grid.com/example/")
        viewport = ".ag-body-viewport"
        await page.wait_for_selector(viewport)

        master_data = {}

        # Horizontal scroll loop
        # We scroll right in 400px chunks until we hit the end
        for v_scroll in range(10):  # Adjust for total rows

            # Reset horizontal to start
            await page.evaluate(f"document.querySelector('{viewport}').scrollLeft = 0")
            await asyncio.sleep(0.5)

            h_pos = 0
            max_h = await page.evaluate(f"document.querySelector('{viewport}').scrollWidth")

            while h_pos < max_h:
                # Capture what is currently visible
                html = await page.content()
                current_batch = extract_ag_grid_smart_merge(html, PINNED_COL_ID)

                # Merge new columns into master records
                for key, data in current_batch.items():
                    if key not in master_data: master_data[key] = {}
                    master_data[key].update(data)

                # Move Right
                h_pos += 400
                await page.evaluate(f"document.querySelector('{viewport}').scrollLeft = {h_pos}")
                await asyncio.sleep(0.6)  # Wait for column virtualization to catch up

            # Move Vertical Down
            await page.evaluate(f"let v = document.querySelector('{viewport}'); v.scrollTop += 500")
            await asyncio.sleep(0.8)


    # 4. Save the final compiled data
    save_table_to_json(master_data, "scraped_results2.json")


if __name__ == "__main__":
    asyncio.run(main())