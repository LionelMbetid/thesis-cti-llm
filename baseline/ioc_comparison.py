import json
from pathlib import Path

# -----------------------------
# Charger le JSON unifié
# -----------------------------
unified_path = Path("results/iocs_unified.json")
with open(unified_path, "r", encoding="utf-8") as f:
    unified = json.load(f)

regex = unified.get("regex", {})
ner = unified.get("ner", {})
llm = unified.get("llm", {})

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
llm_counts = count_iocs(llm)

# -----------------------------
# Affichage comparatif
# -----------------------------
all_keys = set(list(regex.keys()) + list(ner.keys()) + list(llm.keys()))
print(f"{'IoC Type':<12} | {'Regex':<5} | {'spaCy NER':<9} | {'LLM':<5}")
print("-"*40)
for key in all_keys:
    r = regex_counts.get(key, 0)
    n = ner_counts.get(key, 0)
    l = llm_counts.get(key, 0)
    print(f"{key:<12} | {r:<5} | {n:<9} | {l:<5}")

# -----------------------------
# IoCs uniques par méthode
# -----------------------------
unique_regex = {k: set(regex.get(k, [])) - set(llm.get(k, [])) - set(ner.get(k, [])) for k in regex}
unique_ner = {k: set(ner.get(k, [])) - set(llm.get(k, [])) - set(regex.get(k, [])) for k in ner}
unique_llm = {k: set(llm.get(k, [])) - set(regex.get(k, [])) - set(ner.get(k, [])) for k in llm}

# Sauvegarde des uniques
comparison_output = {
    "regex_counts": regex_counts,
    "ner_counts": ner_counts,
    "llm_counts": llm_counts,
    "unique_regex": {k:list(v) for k,v in unique_regex.items()},
    "unique_ner": {k:list(v) for k,v in unique_ner.items()},
    "unique_llm": {k:list(v) for k,v in unique_llm.items()}
}

output_path = Path("results/iocs_comparison.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(comparison_output, f, indent=4)

print("\nIoCs comparison saved to results/iocs_comparison.json")
