# Purpose: Analyze financial discussions and classify sentiment.

import re
from pathlib import Path

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAgent:

    def __init__(self):
        # Initialize sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def clean_text(self, text):
        # Handle missing values
        if pd.isna(text):
            return ""

        # Convert text into string
        text = str(text)

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def analyze_sentiment(self, text):
        # Clean input text
        cleaned_text = self.clean_text(text)

        # Handle empty text
        if not cleaned_text:
            return {
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0
            }

        # Calculate sentiment scores
        scores = self.analyzer.polarity_scores(cleaned_text)

        compound = scores["compound"]

        # Classify sentiment
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "sentiment_score": compound,
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"]
        }

    def process_dataframe(self, df):
        # Check required column
        if "text" not in df.columns:
            raise ValueError("Missing required column: text")

        # Analyze every post
        results = df["text"].apply(self.analyze_sentiment)

        # Convert results into DataFrame
        sentiment_df = pd.DataFrame(
            results.tolist(),
            index=df.index
        )

        # Combine original and sentiment data
        return pd.concat([df.copy(), sentiment_df], axis=1)

    def process_csv(self, input_path, output_path):
        # Convert paths
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Check input file
        if not input_path.exists():
            raise FileNotFoundError(
                f"File not found: {input_path}"
            )

        # Read CSV
        df = pd.read_csv(input_path)

        print("Starting sentiment analysis...")
        print("Total records:", len(df))

        # Process dataset
        result = self.process_dataframe(df)

        # Create output directory
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Save results
        result.to_csv(output_path, index=False)

        print("\nSentiment analysis completed!")
        print("\nSentiment distribution:")
        print(result["sentiment"].value_counts())

        print("\nOutput file:", output_path)

        return result


if __name__ == "__main__":

    # Initialize agent
    agent = SentimentAgent()

    # Find project root directory
    project_root = Path(__file__).resolve().parents[2]

    # Define file paths
    # Define input file containing cleaned Naver discussions
    input_file = (
       project_root
       / "data"
       / "processed"
       / "naver_cleaned.csv"
)

    output_file = (
        project_root
        / "data"
        / "processed"
        / "naver_sentiment.csv"
    )

    # Execute sentiment analysis
    agent.process_csv(input_file, output_file)