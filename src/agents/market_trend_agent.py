# ============================================================
# MARKET TREND ANALYZER AGENT
# Purpose: Analyze overall stock market sentiment using
# sentiment data collected from multiple stocks.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# STEP 1: Define project paths
# ------------------------------------------------------------

INPUT_FILE = Path("data/processed/naver_sentiment.csv")

OUTPUT_FILE = Path("data/processed/market_trend_summary.csv")


# ------------------------------------------------------------
# STEP 2: Load sentiment dataset
# ------------------------------------------------------------

def load_data():

    print("\nLoading sentiment data...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total records loaded: {len(df)}")

    return df


# ------------------------------------------------------------
# STEP 3: Analyze overall sentiment distribution
# ------------------------------------------------------------

def analyze_market_sentiment(df):

    print("\nAnalyzing overall market sentiment...")

    sentiment_counts = df["sentiment"].value_counts()

    total_records = len(df)

    sentiment_percentages = (
        sentiment_counts / total_records
    ) * 100

    print("\nMarket Sentiment Distribution:")

    print(sentiment_counts)

    print("\nMarket Sentiment Percentages:")

    print(sentiment_percentages.round(2))

    return sentiment_counts, sentiment_percentages


# ------------------------------------------------------------
# STEP 4: Calculate market sentiment score
# ------------------------------------------------------------

def calculate_market_score(df):

    print("\nCalculating market sentiment score...")

    positive = (df["sentiment"] == "positive").sum()

    negative = (df["sentiment"] == "negative").sum()

    neutral = (df["sentiment"] == "neutral").sum()

    total = len(df)

    if total == 0:
        raise ValueError("Dataset contains no records.")

    market_score = ((positive - negative) / total) * 100

    if market_score > 5:
        market_condition = "Positive Market Sentiment"

    elif market_score < -5:
        market_condition = "Negative Market Sentiment"

    else:
        market_condition = "Neutral Market Sentiment"

    print(f"\nMarket Sentiment Score: {market_score:.2f}")

    print(f"Market Condition: {market_condition}")

    return market_score, market_condition


# ------------------------------------------------------------
# STEP 5: Generate market summary
# ------------------------------------------------------------

def generate_summary(df):

    sentiment_counts, sentiment_percentages = (
        analyze_market_sentiment(df)
    )

    market_score, market_condition = calculate_market_score(df)

    summary = pd.DataFrame([{

        "total_posts": len(df),

        "positive_posts": int(sentiment_counts.get("positive", 0)),

        "negative_posts": int(sentiment_counts.get("negative", 0)),

        "neutral_posts": int(sentiment_counts.get("neutral", 0)),

        "positive_percentage": round(
            sentiment_percentages.get("positive", 0), 2
        ),

        "negative_percentage": round(
            sentiment_percentages.get("negative", 0), 2
        ),

        "neutral_percentage": round(
            sentiment_percentages.get("neutral", 0), 2
        ),

        "market_score": round(market_score, 2),

        "market_condition": market_condition

    }])

    return summary


# ------------------------------------------------------------
# STEP 6: Save market intelligence report
# ------------------------------------------------------------

def save_results(summary):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(OUTPUT_FILE, index=False)

    print("\nMarket trend analysis completed!")

    print(f"Output saved to: {OUTPUT_FILE}")


# ------------------------------------------------------------
# STEP 7: Main execution
# ------------------------------------------------------------

def main():

    print("\n======================================")
    print(" FINANCIAL MARKET TREND ANALYZER")
    print("======================================")

    df = load_data()

    summary = generate_summary(df)

    print("\nFinal Market Intelligence Report:")

    print(summary.to_string(index=False))

    save_results(summary)


if __name__ == "__main__":

    main()