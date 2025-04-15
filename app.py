import requests
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify

app = Flask(__name__)

FEED_URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=32&file=INTERROGAZIONE.xml"

# Funzione per scaricare e parsare il feed
def get_products():
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
    return products

@app.route("/search", methods=["GET"])
def search():
    query_color = request.args.get("color", "").lower()
    query_size = request.args.get("size", "")
    query_brand = request.args.get("brand", "").lower()
    query_sku = request.args.get("sku", "").lower()

    products = get_products()
    filtered = []

    for p in products:
        if p['availability'] != 'in_stock':
            continue
        if query_sku and query_sku not in p['id'].lower():
            continue
        if query_color and query_color not in p['color'].lower():
            continue
        if query_size and query_size != p['size']:
            continue
        if query_brand and query_brand not in p['brand'].lower():
            continue
        filtered.append(p)

    return jsonify(filtered[:20])

if __name__ == "__main__":
    app.run(debug=True)
