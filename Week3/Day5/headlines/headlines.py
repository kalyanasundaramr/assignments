
import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
}


def get_headlines():
    try:
        response = requests.get(URL, headers=headers, timeout=10)

        # Check the HTTP response before parsing
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find headline elements in the HTML
        items = soup.select("h2, h3")

        headlines = []
        seen = set()

        for item in items:
            headline = item.get_text(" ", strip=True)

            if headline and headline not in seen:
                headlines.append(headline)
                seen.add(headline)

            if len(headlines) == 5:
                break

        if not headlines:
            print("No headlines found. Check the website's HTML or selectors.")
            return

        for number, headline in enumerate(headlines, start=1):
            print(f"{number}. {headline}")

        if len(headlines) < 5:
            print(f"\nOnly {len(headlines)} headlines were found.")

    except requests.exceptions.RequestException as error:
        print(f"Could not fetch the news page: {error}")


if __name__ == "__main__":
    get_headlines()
