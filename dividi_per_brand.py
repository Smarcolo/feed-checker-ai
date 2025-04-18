import json
import os
from unidecode import unidecode

# Crea cartella se non esiste
brand_folder = "brand"
os.makedirs(brand_folder, exist_ok=True)

# Carica catalogo principale
with open("catalogo.json", "r", encoding="utf-8") as f:
    catalogo = json.load(f)

# Raggruppa prodotti per brand
prodotti_per_brand = {}
for prodotto in catalogo:
    brand = unidecode(prodotto.get("brand", "sconosciuto").strip().lower().replace(" ", ""))
    if brand not in prodotti_per_brand:
        prodotti_per_brand[brand] = []
    prodotti_per_brand[brand].append(prodotto)

# Salva ogni brand in un file separato
for brand, prodotti in prodotti_per_brand.items():
    with open(f"{brand_folder}/{brand}.json", "w", encoding="utf-8") as f:
        json.dump(prodotti, f, indent=2, ensure_ascii=False)

print(f"Creati {len(prodotti_per_brand)} file nella cartella /brand")
