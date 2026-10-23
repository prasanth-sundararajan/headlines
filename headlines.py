import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_headlines():
    try:
        # Fetch the page with a timeout
        response = requests.get(URL, headers=headers, timeout=10)
        
        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(f"Error: Failed to fetch page. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find elements containing headlines. 
        # BBC often uses headings like h2 or h3 for news titles.
        raw_items = soup.find_all(["h2", "h3"])
        
        headlines = []
        seen = set()
        
        for item in raw_items:
            text = item.get_text(strip=True)
            # Skip empty entries or duplicates
            if text and text not in seen:
                seen.add(text)
                headlines.append(text)
        
        # Handle the case where fewer than 5 headlines are found
        num_to_print = min(5, len(headlines))
        
        if num_to_print == 0:
            print("No headlines found. The page structure might have changed.")
            return

        print("Top BBC News Headlines:")
        for i in range(num_to_print):
            print(f"{i + 1}. {headlines[i]}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_headlines()