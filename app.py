from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Carica il catalogo light una sola volta (più veloce per GPT e Pabbly)
with open("catalogo_light.json", encoding="utf-8") as f:
    catalogo = json.load(f)

def matches(prodotto, key, value):
    return value.lower() in str(prodotto.get(key, "")).lower()

@app.route("/catalogo", methods=["GET"])
def filtra_catalogo():
    brand = request.args.get("brand")
    size = request.args.get("size")
    color = request.args.get("color")
    gender = request.args.get("gender")
    category = request.args.get("category")
    season = request.args.get("season")

    risultati = catalogo

    if brand:
        risultati = [p for p in risultati if matches(p, "brand", brand)]
    if size:
        risultati = [p for p in risultati if matches(p, "size", size)]
    if color:
        risultati = [p for p in risultati if matches(p, "color", color)]
    if gender:
        risultati = [p for p in risultati if matches(p, "gender", gender)]
    if category:
        risultati = [p for p in risultati if matches(p, "category", category)]
    if season:
        risultati = [p for p in risultati if matches(p, "season", season)]

    # Risposta JSON
    return jsonify({
        "count": len(risultati),
        "results": risultati[:20]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
