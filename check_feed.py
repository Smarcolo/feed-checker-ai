import requests
import xml.etree.ElementTree as ET

def check_feed():
    URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=INTERROGAZIONE.xml"
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Errore nel recupero del feed: {response.status_code}")
        return

    root = ET.fromstring(response.content)

    print("Controllo disponibilità prodotti...")
    for item in root.findall(".//item"):
        product_id = item.find("{http://base.google.com/ns/1.0}id")
        size = item.find("{http://base.google.com/ns/1.0}size")
        availability = item.find("{http://base.google.com/ns/1.0}availability")

        if product_id is not None and size is not None and availability is not None:
            print(f"SKU: {product_id.text}, Taglia: {size.text}, Disponibilità: {availability.text}")

    print("✅ Controllo completato")

if __name__ == '__main__':
    check_feed()
