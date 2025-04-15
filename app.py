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
    query_sku = request.args.get("sku", "").lower()  # 🔍 nuovo campo per ID/SKU

    products = get_products()
    filtered = []

    for p in products:
        if p.get("availability", "").lower() != "in_stock":
            continue
        if query_color and query_color not in p.get("color", "").lower():
            continue
        if query_size and query_size != p.get("size", ""):
            continue
        if query_brand and query_brand not in p.get("brand", "").lower():
            continue
        if query_sku and query_sku.lower() not in p.get("id", "").lower():
            continue
        filtered.append(p)

    return jsonify(filtered[:10])  # massimo 10 risultati

@app.route("/", methods=["GET"])
def home():
    return "✅ Feed Checker AI attivo. Usa /search per interrogare il catalogo."

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
