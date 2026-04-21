# soup_utils.py
from bs4 import BeautifulSoup
import json

def parse_page_data(html_content):
    """
    Takes an HTML string and extracts specific data points.
    Returns a dictionary of results.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Example: Extracting the page title and all H1 text
    data = {
        "title": soup.title.string if soup.title else "No Title",
        "headers": [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
        "links_count": len(soup.find_all('a'))
    }

    return data


def extract_list_items(html_content, css_selector):
    """
    Generic helper to grab text from a list of elements.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.select(css_selector)
    return [item.get_text(strip=True) for item in items]


def extract_ag_grid_data(html_content):
    """Parses visible rows and cells from an ag-Grid HTML snapshot."""
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = []

    # ag-Grid rows typically have the 'ag-row' class
    grid_rows = soup.find_all("div", class_="ag-row")

    for row in grid_rows:
        # Get all cells within this specific row
        cells = row.find_all("div", class_="ag-cell")
        row_data = [cell.get_text(strip=True) for cell in cells]
        if row_data:
            rows.append(tuple(row_data))  # Tuple for set hashing
    return rows


def extract_ag_grid_smart_merge(html_content, key_column_id):
    """
    Scans the entire row, including pinned containers.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    captured_rows = {}

    # Rows in ag-Grid often have an 'aria-rowindex' or 'row-id'
    # that spans across pinned and center sections.
    rows = soup.find_all("div", class_="ag-row")

    for row in rows:
        # This is the secret: row.find_all finds cells in BOTH the
        # pinned container and the center container for this row.
        cells = row.find_all("div", class_="ag-cell")

        row_data = {}
        row_key = None

        for cell in cells:
            cid = cell.get('col-id')
            val = cell.get_text(strip=True)

            if cid:
                row_data[cid] = val
                # Capture our unique key from the pinned column
                if cid == key_column_id:
                    row_key = val

        if row_key:
            captured_rows[row_key] = row_data

    return captured_rows


def save_table_to_json(master_data, filename="ag_grid_full_data.json"):
    """
    Converts the master dictionary (from smart merge) into a
    standard JSON list and saves it to a file.

    :param master_data: Dictionary in format { row_key: { col_id: val } }
    :param filename: String name for the output file
    """
    # Extract just the row dictionaries from our master mapping
    final_list = list(master_data.values())

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(final_list, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(final_list)} rows to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def export_to_json(data_set, headers, filename="ag_grid_export.json"):
    """Maps row tuples to headers and saves as JSON."""
    final_list = [dict(zip(headers, row)) for row in data_set]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    print(f"Done! Exported {len(final_list)} unique rows to {filename}")