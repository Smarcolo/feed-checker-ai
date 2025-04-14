import requests
import xml.etree.ElementTree as ET

def check_feed():
    url = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=INTERROGAZIONE.xml"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Errore nel download: {response.status_code}")
        return

    if not response.text.strip():
        print("⚠️ Il feed è vuoto! Probabilmente Magento non ha ancora generato il file.")
        return

    try:
        root = ET.fromstring(response.content)
        print("✅ Feed scaricato e parsato correttamente")
    except ET.ParseError as e:
        print("❌ Errore nel parsing XML:", e)
