# ============================================================
# FINANCIAL INSIGHTS AGENT
# Purpose: Generate meaningful financial insights using
# stock-wise and overall market sentiment analysis.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# STEP 1: Define input and output paths
# ------------------------------------------------------------

STOCK_FILE = Path("data/processed/stock_sentiment_summary.csv")

MARKET_FILE = Path("data/processed/market_trend_summary.csv")

OUTPUT_FILE = Path("data/processed/financial_insights.txt")


# ------------------------------------------------------------
# STEP 2: Load previous agent outputs
# ------------------------------------------------------------

def load_data():

    print("\nLoading financial analysis data...")

    if not STOCK_FILE.exists():
        raise FileNotFoundError(f"Stock summary not found: {STOCK_FILE}")

    if not MARKET_FILE.exists():
        raise FileNotFoundError(f"Market summary not found: {MARKET_FILE}")

    stock_df = pd.read_csv(STOCK_FILE)

    market_df = pd.read_csv(MARKET_FILE)

    print("Financial data loaded successfully!")

    return stock_df, market_df


# ------------------------------------------------------------
# STEP 3: Generate stock-wise insights
# ------------------------------------------------------------

def generate_stock_insights(stock_df):

    print("\nGenerating stock-wise insights...")

    insights = []

    for _, row in stock_df.iterrows():

        stock_name = row["stockName"]

        positive = row.get("positive", 0)

        negative = row.get("negative", 0)

        neutral = row.get("neutral", 0)

        insights.append(
            f"{stock_name}: {positive}% positive, "
            f"{negative}% negative, "
            f"{neutral}% neutral sentiment."
        )

        if positive > negative:

            insights.append(
                f"{stock_name} has more positive than negative "
                "investor discussions."
            )

        elif negative > positive:

            insights.append(
                f"{stock_name} has more negative than positive "
                "investor discussions."
            )

        else:

            insights.append(
                f"{stock_name} has balanced positive and negative "
                "investor discussions."
            )

    return insights


# ------------------------------------------------------------
# STEP 4: Generate overall market insights
# ------------------------------------------------------------

def generate_market_insights(market_df):

    print("\nGenerating overall market insights...")

    market = market_df.iloc[0]

    total_posts = market["total_posts"]

    positive = market["positive_percentage"]

    negative = market["negative_percentage"]

    neutral = market["neutral_percentage"]

    score = market["market_score"]

    condition = market["market_condition"]

    insights = [

        f"Total analyzed financial discussions: {total_posts}",

        f"Positive sentiment: {positive}%",

        f"Negative sentiment: {negative}%",

        f"Neutral sentiment: {neutral}%",

        f"Overall market sentiment score: {score}",

        f"Overall market condition: {condition}"

    ]

    if neutral > 70:

        insights.append(
            "Most financial discussions are neutral, indicating "
            "limited directional sentiment in this dataset."
        )

    if positive > negative:

        insights.append(
            "Positive discussions exceed negative discussions."
        )

    elif negative > positive:

        insights.append(
            "Negative discussions exceed positive discussions."
        )

    else:

        insights.append(
            "Positive and negative discussions are balanced."
        )

    return insights


# ------------------------------------------------------------
# STEP 5: Generate final financial intelligence report
# ------------------------------------------------------------

def generate_report(stock_insights, market_insights):

    report = []

    report.append("=" * 60)

    report.append("FINANCIAL SENTIMENT INTELLIGENCE REPORT")

    report.append("=" * 60)

    report.append("\n1. STOCK-WISE FINANCIAL INSIGHTS\n")

    report.extend(stock_insights)

    report.append("\n2. OVERALL MARKET INSIGHTS\n")

    report.extend(market_insights)

    report.append("\n" + "=" * 60)

    report.append("END OF FINANCIAL INTELLIGENCE REPORT")

    report.append("=" * 60)

    return "\n".join(report)


# ------------------------------------------------------------
# STEP 6: Save report
# ------------------------------------------------------------

def save_report(report):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(report)

    print("\nFinancial intelligence report generated!")

    print(f"Report saved to: {OUTPUT_FILE}")


# ------------------------------------------------------------
# STEP 7: Main execution
# ------------------------------------------------------------

def main():

    print("\n======================================")

    print(" FINANCIAL INSIGHTS AGENT")

    print("======================================")

    stock_df, market_df = load_data()

    stock_insights = generate_stock_insights(stock_df)

    market_insights = generate_market_insights(market_df)

    report = generate_report(stock_insights, market_insights)

    print("\n" + report)

    save_report(report)


if __name__ == "__main__":

    main()