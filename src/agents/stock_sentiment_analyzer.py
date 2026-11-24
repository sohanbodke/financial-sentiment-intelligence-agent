# PURPOSE: Compare sentiment between Samsung and SK Hynix.

import pandas as pd
from pathlib import Path


def analyze_stock_sentiment():

    # Get the project root directory.
    project_root = Path(__file__).resolve().parents[2]

    # Load sentiment analysis results.
    input_file = (
        project_root
        / "data"
        / "processed"
        / "naver_sentiment.csv"
    )

    df = pd.read_csv(input_file)

    # Display available columns.
    print("\nAvailable columns:")
    print(df.columns.tolist())

    # Compare sentiment distribution by stock.
    print("\nStock-wise sentiment distribution:")

    stock_sentiment = pd.crosstab(
        df["stockName"],
        df["sentiment"]
    )

    print(stock_sentiment)

    # Calculate sentiment percentages.
    print("\nStock-wise sentiment percentages:")

    sentiment_percentage = (
        pd.crosstab(
            df["stockName"],
            df["sentiment"],
            normalize="index"
        ) * 100
    )

    print(sentiment_percentage.round(2))

    # Save the comparison results.
    output_file = (
        project_root
        / "data"
        / "processed"
        / "stock_sentiment_summary.csv"
    )

    sentiment_percentage.to_csv(output_file)

    print("\nAnalysis completed!")
    print(f"Output saved to: {output_file}")


# Execute the analyzer.
if __name__ == "__main__":
    analyze_stock_sentiment()