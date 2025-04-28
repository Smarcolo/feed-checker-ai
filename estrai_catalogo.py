import requests
import xml.etree.ElementTree as ET
import json

# URL del feed XML corretto
url = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=amasty/feed/INTERROGAZIONE.xml"

# Scarica il feed
response = requests.get(url)

# Controlla se la risposta è valida
if response.status_code == 200 and response.content.strip():
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        raise Exception(f"Errore nel parsing dell'XML: {e}")
else:
    raise Exception(f"Errore: il feed non è accessibile o è vuoto. Status code: {response.status_code}")

# Namespace per i tag g:
ns = {'g': 'http://base.google.com/ns/1.0'}

# Lista dei prodotti
prodotti = []

# Estrazione dei dati
for item in root.findall('./channel/item'):
    try:
        prodotti.append({
            "id": item.find('g:id', ns).text,
            "brand": item.find('g:brand', ns).text,
            "title": item.find('title').text.strip(),
            "size": item.find('g:size', ns).text,
            "availability": item.find('g:availability', ns).text,
            "price": item.find('g:price', ns).text,
            "sale_price": item.find('g:sale_price', ns).text if item.find('g:sale_price', ns) is not None else "",
            "color": item.find('g:color', ns).text if item.find('g:color', ns) is not None else "",
            "gender": item.find('g:gender', ns).text if item.find('g:gender', ns) is not None else "",
            "category": item.find('g:custom_label_2', ns).text if item.find('g:custom_label_2', ns) is not None else "",
            "season": item.find('g:custom_label_4', ns).text if item.find('g:custom_label_4', ns) is not None else "",
            "image": item.find('g:image_link', ns).text if item.find('g:image_link', ns) is not None else "",
            "link": item.find('link').text.strip()
        })
    except Exception:
        continue

# Scrive il file JSON
with open("catalogo.json", "w", encoding="utf-8") as f:
    json.dump(prodotti, f, indent=2, ensure_ascii=False)
