import requests
import xml.etree.ElementTree as ET
import json

FEED_URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=amasty/feed/INTERROGAZIONE.xml"
XML_FILE = "catalogo.xml"
JSON_FILE = "catalogo.json"

def check_feed():
    # Scarica il file XML e salvalo in locale
    print("📥 Scarico il feed...")
    response = requests.get(FEED_URL)
    if response.status_code != 200 or not response.content.strip():
        raise Exception(f"Errore durante il download del feed: Status code {response.status_code}, feed vuoto o non valido.")

    with open(XML_FILE, "wb") as f:
        f.write(response.content)

    # Parsing XML da file
    print("🔍 Leggo il file XML locale...")
    try:
        tree = ET.parse(XML_FILE)
    except ET.ParseError as e:
        raise Exception(f"Errore nel parsing del file XML locale: {e}")

    root = tree.getroot()
    items = root.findall('.//item')

    namespaces = {'g': 'http://base.google.com/ns/1.0'}
    products = []

    for item in items:
        product = {
            "id": item.findtext('g:id', default='', namespaces=namespaces),
            "title": item.findtext('title', default=''),
            "description": item.findtext('description', default=''),
            "link": item.findtext('link', default=''),
            "image": item.findtext('g:image_link', default='', namespaces=namespaces),
            "price": item.findtext('g:price', default='', namespaces=namespaces),
            "sale_price": item.findtext('g:sale_price', default='', namespaces=namespaces),
            "availability": item.findtext('g:availability', default='', namespaces=namespaces),
            "brand": item.findtext('g:brand', default='', namespaces=namespaces),
            "size": item.findtext('g:size', default='', namespaces=namespaces),
            "color": item.findtext('g:color', default='', namespaces=namespaces)
        }
        products.append(product)

    # Salva il file JSON
    print(f"💾 Salvo {len(products)} prodotti in {JSON_FILE}...")
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print("✅ Fatto!")

check_feed()
