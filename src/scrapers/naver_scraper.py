# Purpose: Collect Korean stock discussions using Apify.

import os
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

# IMPORTANT:
# Verify this Actor ID and its input schema in Apify Console.
ACTOR_ID = "hgservices/naver-stock-discussion-scraper"


# --------------------------------------------------
# 2. Configure project directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. Korean stocks to monitor
# --------------------------------------------------

STOCKS = [
    "005930",  # Samsung Electronics
    "000660"   # SK Hynix
]


# --------------------------------------------------
# 4. Create Apify scraping function
# --------------------------------------------------

def scrape_naver():

    print("\nStarting Naver Finance Scraper...")

    # Check API token
    if not APIFY_TOKEN:
        raise ValueError("Apify API token is missing.")

    # Connect to Apify
    client = ApifyClient(APIFY_TOKEN)

    # Calculate last 10 days
    today = datetime.now(
        ZoneInfo("Asia/Seoul")
    ).date()

    start_date = (
        today - timedelta(days=10)
    ).isoformat()

    print("Stocks:", STOCKS)
    print("Start date:", start_date)

    # --------------------------------------------------
    # 5. Execute Apify Actor
    # --------------------------------------------------

    print("\nExecuting Apify Actor...")

    # This is a connectivity/basic execution test.
    # Add the Actor's documented input parameters here.
    run = client.actor(ACTOR_ID).call(

    run_input={

        "stocks": STOCKS

    }

   )

    if not run:
        raise RuntimeError(
            "Apify Actor execution failed."
        )

    print("Actor execution completed.")

    # --------------------------------------------------
    # 6. Retrieve scraped dataset
    # --------------------------------------------------

    # Retrieve dataset ID from Apify Run object

    dataset_id = run.default_dataset_id

    if not dataset_id:

        raise RuntimeError(

        "No dataset ID returned by Apify."


    )

    dataset_items = list(
        client.dataset(dataset_id).iterate_items()
    )

    print("Total records:", len(dataset_items))

    if not dataset_items:
        print("No records found.")
        return

    # --------------------------------------------------
    # 7. Convert data into DataFrame
    # --------------------------------------------------

    df = pd.DataFrame(dataset_items)

    # --------------------------------------------------
    # 8. Save raw data
    # --------------------------------------------------

    output_file = (
        OUTPUT_DIR / "naver_stock_discussions.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nScraping completed!")
    print("Total records:", len(df))
    print("Saved file:", output_file)

    # --------------------------------------------------
    # 9. Display sample records
    # --------------------------------------------------

    print("\nSample records:")

    print(df.head())


# --------------------------------------------------
# 10. Main execution
# --------------------------------------------------

if __name__ == "__main__":

    scrape_naver()