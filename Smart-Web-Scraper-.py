import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "http://quotes.toscrape.com/page/{}/"

def fetch_page(page_number):
    url = BASE_URL.format(page_number)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page {page_number}")
        return None


def parse_data(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    data = []
    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]

        data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })

    return data


def save_to_csv(all_data):
    keys = ["Quote", "Author", "Tags"]

    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_data)


def scrape():
    all_quotes = []

    for page in range(1, 6):
        print(f"Scraping page {page}...")
        html = fetch_page(page)

        if html:
            page_data = parse_data(html)
            all_quotes.extend(page_data)

        time.sleep(1)

    save_to_csv(all_quotes)
    print("Scraping completed! Data saved to quotes.csv")


def read_csv():
    with open("quotes.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            print("Quote:", row["Quote"])
            print("Author:", row["Author"])
            print("Tags:", row["Tags"])
            print("-" * 50)


if __name__ == "__main__":
    scrape()
    read_csv()
