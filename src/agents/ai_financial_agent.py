# ============================================================
# FREE AI FINANCIAL INTELLIGENCE AGENT
# Purpose:
# Analyze financial sentiment without paid API calls.
# Uses Python and existing project CSV datasets.
# ============================================================

import csv
from pathlib import Path
from collections import defaultdict


# ------------------------------------------------------------
# STEP 1: Define project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SENTIMENT_FILE = (
    PROJECT_ROOT /
    "data/processed/naver_sentiment.csv"
)

STOCK_FILE = (
    PROJECT_ROOT /
    "data/processed/stock_sentiment_summary.csv"
)

MARKET_FILE = (
    PROJECT_ROOT /
    "data/processed/market_trend_summary.csv"
)

INSIGHTS_FILE = (
    PROJECT_ROOT /
    "data/processed/financial_insights.txt"
)


# ------------------------------------------------------------
# STEP 2: Read CSV files
# ------------------------------------------------------------

def read_csv_file(file_path):

    if not file_path.exists():
        return []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


# ------------------------------------------------------------
# STEP 3: Load financial intelligence data
# ------------------------------------------------------------

def load_financial_data():

    print("\nLoading financial intelligence data...")

    sentiment_data = read_csv_file(SENTIMENT_FILE)

    stock_data = read_csv_file(STOCK_FILE)

    market_data = read_csv_file(MARKET_FILE)

    insights = ""

    if INSIGHTS_FILE.exists():

        insights = INSIGHTS_FILE.read_text(
            encoding="utf-8"
        )

    print("Financial data loaded successfully!")

    print(f"Sentiment records: {len(sentiment_data)}")

    print(f"Stocks analyzed: {len(stock_data)}")

    print(f"Market records: {len(market_data)}")

    return sentiment_data, stock_data, market_data, insights


# ------------------------------------------------------------
# STEP 4: Analyze individual stocks
# ------------------------------------------------------------

def analyze_stocks(sentiment_data):

    stock_results = defaultdict(
        lambda: {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "score_sum": 0,
            "score_count": 0
        }
    )

    for row in sentiment_data:

        stock = (
            row.get("stockName")
            or row.get("stockCode")
            or "Unknown"
        )

        sentiment = (
            row.get("sentiment", "neutral")
            .strip()
            .lower()
        )

        result = stock_results[stock]

        result["total"] += 1

        if sentiment in ["positive", "negative", "neutral"]:

            result[sentiment] += 1

        try:

            score = float(
                row.get("sentiment_score", "")
            )

            result["score_sum"] += score

            result["score_count"] += 1

        except (ValueError, TypeError):

            pass

    for stock, result in stock_results.items():

        total = result["total"]

        result["positive_pct"] = (
            result["positive"] / total * 100
            if total else 0
        )

        result["negative_pct"] = (
            result["negative"] / total * 100
            if total else 0
        )

        result["neutral_pct"] = (
            result["neutral"] / total * 100
            if total else 0
        )

        result["average_score"] = (
            result["score_sum"] / result["score_count"]
            if result["score_count"] else None
        )

    return stock_results


# ------------------------------------------------------------
# STEP 5: Analyze overall market sentiment
# ------------------------------------------------------------

def analyze_market(stock_results, market_data):

    total = sum(
        data["total"]
        for data in stock_results.values()
    )

    positive = sum(
        data["positive"]
        for data in stock_results.values()
    )

    negative = sum(
        data["negative"]
        for data in stock_results.values()
    )

    neutral = sum(
        data["neutral"]
        for data in stock_results.values()
    )

    if total == 0:

        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "condition": "Insufficient Data"
        }

    positive_pct = positive / total * 100

    negative_pct = negative / total * 100

    neutral_pct = neutral / total * 100

    if positive_pct > negative_pct and positive_pct >= neutral_pct:

        condition = "Positive Market Sentiment"

    elif negative_pct > positive_pct and negative_pct >= neutral_pct:

        condition = "Negative Market Sentiment"

    else:

        condition = "Neutral Market Sentiment"

    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "neutral_pct": neutral_pct,
        "condition": condition
    }


# ------------------------------------------------------------
# STEP 6: Display stock analysis
# ------------------------------------------------------------

def display_stock_analysis(stock_results):

    print("\n========== STOCK SENTIMENT ANALYSIS ==========")

    for stock, data in stock_results.items():

        print(f"\nStock: {stock}")

        print(f"Total Posts: {data['total']}")

        print(f"Positive: {data['positive']} ({data['positive_pct']:.2f}%)")

        print(f"Negative: {data['negative']} ({data['negative_pct']:.2f}%)")

        print(f"Neutral: {data['neutral']} ({data['neutral_pct']:.2f}%)")

        if data["average_score"] is not None:

            print(
                f"Average Sentiment Score: "
                f"{data['average_score']:.4f}"
            )


# ------------------------------------------------------------
# STEP 7: Compare Samsung and SK Hynix
# ------------------------------------------------------------

def compare_stocks(stock_results):

    print("\n========== STOCK COMPARISON ==========")

    if len(stock_results) < 2:

        print("Not enough stock data for comparison.")

        return

    ranked_stocks = sorted(
        stock_results.items(),
        key=lambda item: (
            item[1]["positive_pct"],
            -item[1]["negative_pct"]
        ),
        reverse=True
    )

    for stock, data in ranked_stocks:

        print(f"\n{stock}")

        print(
            f"Positive Sentiment: "
            f"{data['positive_pct']:.2f}%"
        )

        print(
            f"Negative Sentiment: "
            f"{data['negative_pct']:.2f}%"
        )

        print(
            f"Neutral Sentiment: "
            f"{data['neutral_pct']:.2f}%"
        )

    best_stock, best_data = ranked_stocks[0]

    print("\nCOMPARISON RESULT:")

    if best_data["positive_pct"] == ranked_stocks[1][1]["positive_pct"]:

        print("Both stocks have equal positive sentiment.")

    else:

        print(
            f"{best_stock} has the higher positive "
            f"sentiment percentage."
        )

    print(
        "\nNote: This is a sentiment comparison, "
        "not a stock performance prediction."
    )


# ------------------------------------------------------------
# STEP 8: Generate market analysis
# ------------------------------------------------------------

def generate_market_report(market):

    print("\n========== MARKET INTELLIGENCE ==========")

    print(f"Total Posts: {market['total']}")

    print(f"Positive Posts: {market['positive']}")

    print(f"Negative Posts: {market['negative']}")

    print(f"Neutral Posts: {market['neutral']}")

    if market["total"] > 0:

        print(
            f"Positive Percentage: "
            f"{market['positive_pct']:.2f}%"
        )

        print(
            f"Negative Percentage: "
            f"{market['negative_pct']:.2f}%"
        )

        print(
            f"Neutral Percentage: "
            f"{market['neutral_pct']:.2f}%"
        )

    print(f"\nMarket Condition: {market['condition']}")


# ------------------------------------------------------------
# STEP 9: Generate financial intelligence report
# ------------------------------------------------------------

def generate_financial_report(stock_results, market):

    report = []

    report.append("=" * 60)

    report.append("FINANCIAL INTELLIGENCE REPORT")

    report.append("=" * 60)

    report.append("\n1. STOCK-WISE ANALYSIS")

    for stock, data in stock_results.items():

        report.append(f"\nStock: {stock}")

        report.append(f"Total Posts: {data['total']}")

        report.append(
            f"Positive: {data['positive_pct']:.2f}%"
        )

        report.append(
            f"Negative: {data['negative_pct']:.2f}%"
        )

        report.append(
            f"Neutral: {data['neutral_pct']:.2f}%"
        )

    report.append("\n2. OVERALL MARKET ANALYSIS")

    report.append(
        f"Total Posts: {market['total']}"
    )

    report.append(
        f"Market Condition: {market['condition']}"
    )

    report.append("\n3. KEY FINDINGS")

    report.append(
        "Analysis is based on collected investor discussions."
    )

    report.append(
        "Sentiment does not guarantee future stock performance."
    )

    report.append(
        "The sample size and language-model limitations "
        "should be considered."
    )

    report_text = "\n".join(report)

    output_file = (
        PROJECT_ROOT /
        "data/processed/local_financial_report.txt"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file.write_text(
        report_text,
        encoding="utf-8"
    )

    print("\n" + report_text)

    print(f"\nReport saved to: {output_file}")


# ------------------------------------------------------------
# STEP 10: Interactive financial agent
# ------------------------------------------------------------

def answer_question(question, stock_results, market):

    question = question.lower()

    if any(
        word in question
        for word in ["compare", "comparison", "samsung", "hynix"]
    ):

        compare_stocks(stock_results)

    elif any(
        word in question
        for word in ["market", "overall", "trend"]
    ):

        generate_market_report(market)

    elif any(
        word in question
        for word in ["report", "financial intelligence"]
    ):

        generate_financial_report(
            stock_results,
            market
        )

    elif any(
        word in question
        for word in ["which stock", "better", "best", "ranking"]
    ):

        compare_stocks(stock_results)

    elif any(
        word in question
        for word in ["show stocks", "stock analysis", "sentiment"]
    ):

        display_stock_analysis(stock_results)

    else:

        print("\nI can help you with:")

        print("1. Stock sentiment analysis")

        print("2. Samsung vs SK Hynix comparison")

        print("3. Overall market sentiment")

        print("4. Financial intelligence report")


# ------------------------------------------------------------
# STEP 11: Main application
# ------------------------------------------------------------

def main():

    print("\n======================================")

    print(" FREE FINANCIAL INTELLIGENCE AGENT ")

    print("======================================")

    sentiment_data, stock_data, market_data, insights = (
        load_financial_data()
    )

    if not sentiment_data and not stock_data:

        print("\nNo sentiment data available.")

        print("Run the sentiment analysis pipeline first.")

        return

    stock_results = analyze_stocks(sentiment_data)

    market = analyze_market(
        stock_results,
        market_data
    )

    print("\nFinancial Intelligence Agent is ready!")

    print("\nAvailable questions:")

    print("1. Compare Samsung and SK Hynix.")

    print("2. What is the overall market sentiment?")

    print("3. Which stock has better investor sentiment?")

    print("4. Show stock sentiment analysis.")

    print("5. Generate a financial intelligence report.")

    print("\nType 'exit' to stop the agent.")

    while True:

        question = input(
            "\nAsk your financial question: "
        ).strip()

        if question.lower() in ["exit", "quit"]:

            print("\nClosing Financial Intelligence Agent...")

            break

        if not question:

            print("Please enter a question.")

            continue

        try:

            answer_question(
                question,
                stock_results,
                market
            )

        except Exception as error:

            print("\nAnalysis failed:")

            print(error)


# ------------------------------------------------------------
# STEP 12: Execute application
# ------------------------------------------------------------

if __name__ == "__main__":

    main()