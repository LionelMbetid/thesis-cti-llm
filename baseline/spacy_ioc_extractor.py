import spacy
import json
from pathlib import Path

# -----------------------------
# Charger le modèle spaCy
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Charger le rapport CTI
# -----------------------------
input_path = Path("data/sample_report.txt")
text = input_path.read_text(encoding="utf-8")

# -----------------------------
# Extraire les entités nommées
# -----------------------------
doc = nlp(text)

entities = {}
for ent in doc.ents:
    if ent.label_ not in entities:
        entities[ent.label_] = []
    entities[ent.label_].append(ent.text)

# Supprimer les doublons
for k in entities:
    entities[k] = list(set(entities[k]))

# -----------------------------
# Sauvegarder les résultats
# -----------------------------
output_path = Path("results/iocs_spacy.json")
output_path.parent.mkdir(exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=4)

print("Entities extracted with spaCy NER:")
for k, v in entities.items():
    print(f"{k}: {len(v)} found")
