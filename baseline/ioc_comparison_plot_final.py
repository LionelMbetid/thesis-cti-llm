import json
import matplotlib.pyplot as plt

# -----------------------------
# Charger le JSON de comparaison final
# -----------------------------
with open("results/iocs_comparison_final.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tri des labels pour cohérence
labels = sorted(data["regex_counts"].keys())

# Comptage par méthode
regex_counts = [data["regex_counts"].get(k,0) for k in labels]
ner_counts   = [data["ner_counts"].get(k,0) for k in labels]
bert_counts  = [data["bert_counts"].get(k,0) for k in labels]

# Position sur l'axe X
x = range(len(labels))
width = 0.25

# -----------------------------
# Création du graphique
# -----------------------------
plt.figure(figsize=(12,6))

plt.bar([i-width for i in x], regex_counts, width=width, label="Regex")
plt.bar(x, ner_counts, width=width, label="spaCy NER")
plt.bar([i+width for i in x], bert_counts, width=width, label="BERT NER")

plt.xticks(x, labels, rotation=45)
plt.ylabel("Nombre d'IoCs")
plt.title("Comparaison IoCs : Regex vs spaCy vs BERT (URLs et CVE inclus)")
plt.legend()
plt.tight_layout()

# Affichage du graphique
plt.show()
