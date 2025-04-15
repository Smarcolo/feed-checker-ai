import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Legge il file catalogo.json già aggiornato
def get_products():
    with open("catalogo.json", "r", encoding="utf-8") as f:
        return json.load(f)

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

@app.route("/", methods=["GET"])
def home():
    return "✅ Feed Checker AI attivo. Usa /search per interrogare il catalogo."

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
