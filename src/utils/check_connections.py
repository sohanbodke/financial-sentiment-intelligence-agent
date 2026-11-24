# Purpose: Verify Apify and Exa API connectivity.

import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from exa_py import Exa

# Load environment variables
load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
EXA_API_KEY = os.getenv("EXA_API_KEY")


# Check Apify connection
def check_apify():

    print("\nChecking Apify connection...")

    if not APIFY_TOKEN:
        print("Apify token missing!")
        return

    try:
        client = ApifyClient(APIFY_TOKEN)

        user = client.user().get()

        print("Apify connected successfully!")
        print("Account:", user.username)

    except Exception as error:
        print("Apify connection failed:", error)


# Check Exa connection
def check_exa():

    print("\nChecking Exa connection...")

    if not EXA_API_KEY:
        print("Exa API key missing!")
        return

    try:
        exa = Exa(api_key=EXA_API_KEY)

        results = exa.search(
            "Latest financial news about Samsung Electronics",
            num_results=1
        )

        print("Exa connected successfully!")

        for result in results.results:
            print("News:", result.title)

    except Exception as error:
        print("Exa connection failed:", error)


# Main execution
if __name__ == "__main__":

    check_apify()
    check_exa()