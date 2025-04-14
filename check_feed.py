import requests
import xml.etree.ElementTree as ET
import json

FEED_URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=INTERROGAZIONE.xml"

def check_feed():
    response = requests.get(FEED_URL)
    root = ET.fromstring(response.content)
    items = root.findall('.//item')

    products = []
    for item in items:
        namespaces = {'g': 'http://base.google.com/ns/1.0'}
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

    with open("catalogo.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

check_feed()
