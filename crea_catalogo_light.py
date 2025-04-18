import json

# Carica il catalogo originale
with open("catalogo.json", "r", encoding="utf-8") as f:
    catalogo = json.load(f)

# Seleziona solo i campi principali
campi_utili = [
    "id", "title", "brand", "size", "price", "sale_price",
    "color", "gender", "category", "season", "image", "link"
]

# Crea il catalogo light
catalogo_light = []

for prodotto in catalogo:
    prodotto_light = {campo: prodotto.get(campo, "") for campo in campi_utili}
    catalogo_light.append(prodotto_light)

# Salva il file
with open("catalogo_light.json", "w", encoding="utf-8") as f:
    json.dump(catalogo_light, f, ensure_ascii=False, indent=2)

print("✅ catalogo_light.json generato con successo.")
