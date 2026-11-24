# Purpose: Clean, standardize and prepare Naver stock discussions
# for financial sentiment analysis.

import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data/raw/naver_stock_discussions.csv"

OUTPUT_FILE = BASE_DIR / "data/processed/naver_cleaned.csv"


# --------------------------------------------------
# 2. Load raw data
# --------------------------------------------------

def clean_naver_data():

    print("\nStarting Naver Data Cleaning...")

    # Preserve stock codes as strings
    df = pd.read_csv(
        INPUT_FILE,
        dtype={"stockCode": str}
    )

    print("Original records:", len(df))


    # --------------------------------------------------
    # 3. Normalize stock codes
    # --------------------------------------------------

    df["stockCode"] = df["stockCode"].str.zfill(6)


    # --------------------------------------------------
    # 4. Convert timestamps to UTC
    # --------------------------------------------------

    df["timestamp_utc"] = pd.to_datetime(
        df["writtenAt"],
        utc=True,
        errors="coerce"
    )

    df["scrapedAt"] = pd.to_datetime(
        df["scrapedAt"],
        utc=True,
        errors="coerce"
    )


    # --------------------------------------------------
    # 5. Remove invalid timestamps
    # --------------------------------------------------

    df = df.dropna(
        subset=["timestamp_utc"]
    )


    # --------------------------------------------------
    # 6. Filter last 10 days
    # Use latest scraping timestamp as snapshot reference.
    # --------------------------------------------------

    reference_time = df["scrapedAt"].max()

    if pd.isna(reference_time):
        reference_time = pd.Timestamp.now(tz="UTC")

    start_time = reference_time - pd.Timedelta(days=10)

    df = df[
        (df["timestamp_utc"] >= start_time) &
        (df["timestamp_utc"] <= reference_time + pd.Timedelta(minutes=5))
    ].copy()


    # --------------------------------------------------
    # 7. Clean text fields
    # --------------------------------------------------

    df["title"] = df["title"].fillna("").astype(str)

    df["text"] = df["text"].fillna("").astype(str)

    df["full_text"] = (
        df["title"] + " " + df["text"]
    ).str.strip()

    df = df[df["full_text"] != ""]


    # --------------------------------------------------
    # 8. Clean engagement metrics
    # --------------------------------------------------

    engagement_columns = [
        "views",
        "likes",
        "dislikes"
    ]

    for column in engagement_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)


    # --------------------------------------------------
    # 9. Remove duplicate posts
    # --------------------------------------------------

    df = df.drop_duplicates(
        subset=["stockCode", "postId"]
    )


    # --------------------------------------------------
    # 10. Create engagement score
    # --------------------------------------------------

    df["engagement_score"] = (
        df["likes"] * 2 +
        df["dislikes"] +
        df["views"] * 0.01
    )


    # --------------------------------------------------
    # 11. Select standardized columns
    # --------------------------------------------------

    final_columns = [
        "stockCode",
        "stockName",
        "timestamp_utc",
        "title",
        "text",
        "full_text",
        "author",
        "views",
        "likes",
        "dislikes",
        "engagement_score",
        "isHolderVerified",
        "url"
    ]

    df = df[final_columns]


    # --------------------------------------------------
    # 12. Save cleaned dataset
    # --------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )


    # --------------------------------------------------
    # 13. Display cleaning report
    # --------------------------------------------------

    print("\nData Cleaning Completed!")

    print("Clean records:", len(df))

    print("\nStock distribution:")

    print(
        df["stockCode"].value_counts()
    )

    print("\nMissing values:")

    print(
        df.isnull().sum()
    )

    print("\nSaved file:", OUTPUT_FILE)

    print("\nSample cleaned data:")

    print(df.head(3).to_string())


# --------------------------------------------------
# 14. Main execution
# --------------------------------------------------

if __name__ == "__main__":

    clean_naver_data()
    