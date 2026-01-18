import re
import json
from pathlib import Path
import spacy
from transformers import pipeline

# -----------------------------
# Initialisation
# -----------------------------
# spaCy NLP
nlp = spacy.load("en_core_web_sm")

# LLM HuggingFace pipeline (extraction de texte)
# Ici on utilise un modèle de type "text2text-generation"
llm = pipeline("text2text-generation", model="google/flan-t5-small")  # léger pour test local

# -----------------------------
# Regex patterns
# -----------------------------
REGEX_PATTERNS = {
    "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "domain": r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
}

# -----------------------------
# Charger le rapport CTI
# -----------------------------
input_path = Path("data/sample_report.txt")
text = input_path.read_text(encoding="utf-8")

# -----------------------------
# Extraction Regex
# -----------------------------
regex_iocs = {}
for ioc_type, pattern in REGEX_PATTERNS.items():
    matches = re.findall(pattern, text)
    regex_iocs[ioc_type] = list(set(matches))

# -----------------------------
# Extraction spaCy NER
# -----------------------------
doc = nlp(text)
ner_entities = {}
for ent in doc.ents:
    if ent.label_ not in ner_entities:
        ner_entities[ent.label_] = []
    ner_entities[ent.label_].append(ent.text)
# supprimer les doublons
for k in ner_entities:
    ner_entities[k] = list(set(ner_entities[k]))

# -----------------------------
# Extraction LLM
# -----------------------------
prompt = f"Extract all cybersecurity IoCs (IP, domain, hashes, malware names) from this text:\n{text}\nReturn as JSON with keys: ipv4, domain, md5, sha1, sha256, malware_name."
llm_output = llm(prompt, max_length=512)[0]['generated_text']

try:
    llm_iocs = json.loads(llm_output)
except:
    llm_iocs = {"error": "LLM output could not be parsed as JSON", "raw": llm_output}

# -----------------------------
# Fusion des résultats
# -----------------------------
unified_iocs = {
    "regex": regex_iocs,
    "ner": ner_entities,
    "llm": llm_iocs
}

# -----------------------------
# Sauvegarder JSON unifié
# -----------------------------
output_path = Path("results/iocs_unified.json")
output_path.parent.mkdir(exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(unified_iocs, f, indent=4)

print("Unified IoCs extracted and saved to results/iocs_unified.json")
