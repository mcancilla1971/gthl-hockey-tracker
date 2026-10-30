import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://gthlcanada.com/standing/"
OUTPUT = Path("gthl_u12_aa_standings.csv")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_timeout(5000)
    frame = next(
        f for f in page.frames
        if "standings.aspx" in f.url
    )

    frame.locator("#ddlDiv").select_option("U12")
    frame.locator("#ddlCat").select_option("A2")

    all_rows = []

    for region in ["West", "East"]:
        frame.locator("#ddlRegion").select_option(
            label=region
        )

        frame.wait_for_timeout(3000)
        frame.locator("table").first.wait_for()

        headers = frame.locator("table").first.locator(
            "thead th"
        ).all_inner_texts()

        rows = frame.locator("table").first.locator(
            "tbody tr"
        ).all()

        for row in rows:
            cells = row.locator("td").all_inner_texts()
            if cells:
                all_rows.append([region] + cells)

        print(f"{region}: {len(rows)} rows found")

    if len(all_rows) < 23:
        raise RuntimeError("Incomplete standings: fewer than 23 teams. CSV preserved.")

    with OUTPUT.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Region"] + headers)
        writer.writerows(all_rows)

    browser.close()

print(f"Saved {len(all_rows)} teams to {OUTPUT}")
