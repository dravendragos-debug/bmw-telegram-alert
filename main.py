import time
import requests
from bs4 import BeautifulSoup

# Telegram bot config
TELEGRAM_TOKEN = "7742144353:AAEaaOQBJlgrpxXrvwRDx1A077hmm0Oq_uU"
CHAT_ID = "6556990470"

# Mobile.de search URLs
SEARCHES = [
    {
        "name": "BMW Seria 3 M Paket",
        "url": "https://suchen.mobile.de/fahrzeuge/search.html?isSearchRequest=true&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=9&minFirstRegistrationDate=2020-01-01&maxPrice=26000&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=EXPORT&grossPrice=true",
        "keywords": ["M Paket"]
    },
    {
        "name": "BMW X3 M Paket Laser",
        "url": "https://suchen.mobile.de/fahrzeuge/search.html?isSearchRequest=true&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=21&minFirstRegistrationDate=2020-01-01&maxPrice=35000&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=EXPORT&grossPrice=true",
        "keywords": ["M Paket", "Laser"]
    },
    {
        "name": "Volvo XC60 R-Design",
        "url": "https://suchen.mobile.de/fahrzeuge/search.html?isSearchRequest=true&makeModelVariant1.makeId=25100&makeModelVariant1.modelId=67&minFirstRegistrationDate=2020-01-01&maxPrice=27000&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=EXPORT&grossPrice=true",
        "keywords": ["R-Design"]
    },
]

sent_ads = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

def check_search(search):
    response = requests.get(search["url"])
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select(".cBox-body.cBox-body--resultitem")

    for listing in listings:
        link = listing.select_one("a")
        title = listing.select_one(".h3.text-module-begin")
        price = listing.select_one(".price-block")

        if not link or not title:
            continue

        ad_url = "https://mobile.de" + link["href"]
        if ad_url in sent_ads:
            continue

        text = title.get_text(strip=True).lower()
        if all(keyword.lower() in text for keyword in search["keywords"]):
            message = f"🚘 <b>{search['name']}</b>\n💶 {price.get_text(strip=True)}\n🔗 <a href=\"{ad_url}\">Vezi anunț</a>"
            send_telegram(message)
            sent_ads.add(ad_url)

if __name__ == "__main__":
    while True:
        for search in SEARCHES:
            try:
                check_search(search)
            except Exception as e:
                print(f"Eroare la căutarea {search['name']}: {e}")
        time.sleep(600)  # verifică la fiecare 10 minute
