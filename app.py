from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

FEED_URL = "https://www.langolo-calzature.it/it/amfeed/feed/download?id=13&file=MAGENTO%20-%20GOOGLE.xml"

def parse_feed():
    response = requests.get(FEED_URL)
    response.encoding = 'utf-8'
    xml_content = response.text
    root = ET.fromstring(xml_content)

    items = []
    for item in root.findall(".//item"):
        items.append({
            'id': item.findtext('g:id'),
            'title': item.findtext('title'),
            'brand': item.findtext('g:brand'),
            'size': item.findtext('g:size'),
            'availability': item.findtext('g:availability'),
            'link': item.findtext('link')
        })
    return items

@app.route('/')
def home():
    return "Feed Checker AI attivo! 🚀"

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
