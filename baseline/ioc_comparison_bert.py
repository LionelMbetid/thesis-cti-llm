import json
from pathlib import Path

# -----------------------------
# Charger le JSON unifié BERT
# -----------------------------
unified_path = Path("results/iocs_unified_bert.json")
with open(unified_path, "r", encoding="utf-8") as f:
    unified = json.load(f)

regex = unified.get("regex", {})
ner = unified.get("ner", {})
bert = unified.get("bert_ner", {})

# -----------------------------
# Fonction pour compter IoCs
# -----------------------------
def count_iocs(iocs_dict):
    counts = {}
    for k, v in iocs_dict.items():
        if isinstance(v, list):
            counts[k] = len(v)
        else:
            counts[k] = "N/A"
    return counts

# -----------------------------
# Comptage par méthode
# -----------------------------
regex_counts = count_iocs(regex)
ner_counts = count_iocs(ner)
bert_counts = count_iocs(bert)

# -----------------------------
# Affichage comparatif
# -----------------------------
all_keys = set(list(regex.keys()) + list(ner.keys()) + list(bert.keys()))
print(f"{'IoC Type':<12} | {'Regex':<5} | {'spaCy NER':<9} | {'BERT':<5}")
print("-"*40)
for key in all_keys:
    r = regex_counts.get(key, 0)
    n = ner_counts.get(key, 0)
    b = bert_counts.get(key, 0)
    print(f"{key:<12} | {r:<5} | {n:<9} | {b:<5}")

# -----------------------------
# IoCs uniques par méthode
# -----------------------------
unique_regex = {k: set(regex.get(k, [])) - set(ner.get(k, [])) - set(bert.get(k, [])) for k in regex}
unique_ner = {k: set(ner.get(k, [])) - set(regex.get(k, [])) - set(bert.get(k, [])) for k in ner}
unique_bert = {k: set(bert.get(k, [])) - set(regex.get(k, [])) - set(ner.get(k, [])) for k in bert}

# Sauvegarde des uniques
comparison_output = {
    "regex_counts": regex_counts,
    "ner_counts": ner_counts,
    "bert_counts": bert_counts,
    "unique_regex": {k:list(v) for k,v in unique_regex.items()},
    "unique_ner": {k:list(v) for k,v in unique_ner.items()},
    "unique_bert": {k:list(v) for k,v in unique_bert.items()}
}

output_path = Path("results/iocs_comparison_bert.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(comparison_output, f, indent=4)

print("\nIoCs comparison saved to results/iocs_comparison_bert.json")
