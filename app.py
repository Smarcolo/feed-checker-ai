from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

FEED_URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=13&file=MAGENTO%20-%20GOOGLE.xml"
NS = {'g': 'http://base.google.com/ns/1.0'}  # Namespace Google

def parse_feed():
    response = requests.get(FEED_URL)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)

    items = []
    for item in root.findall(".//item"):
        items.append({
            'id': item.findtext('g:id', default='', namespaces=NS),
            'title': item.findtext('title', default=''),
            'brand': item.findtext('g:brand', default='', namespaces=NS),
            'availability': item.findtext('g:availability', default='', namespaces=NS),
            'price': item.findtext('g:price', default='', namespaces=NS),
            'link': item.findtext('link', default=''),
            'image': item.findtext('g:image_link', default='', namespaces=NS)
        })
    return items

@app.route('/')
def home():
    return "Feed Checker AI aggiornato con availability e brand! 🚀"

@app.route('/check', methods=['GET'])
def check_product():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    items = parse_feed()
    results = [item for item in items if query in (item['title'] or '').lower()]

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

