import re
import json
from pathlib import Path
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# -----------------------------
# Initialisation spaCy
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Initialisation BERT NER
# -----------------------------
model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
bert_ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# -----------------------------
# Regex patterns pour IoCs techniques + URLs + CVE
# -----------------------------
REGEX_PATTERNS = {
    "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "domain": r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
    "url": r"\bhttps?://[^\s]+",                 # HTTP/HTTPS URL
    "cve": r"\bCVE-\d{4}-\d{4,7}\b"              # Ex. CVE-2023-12345
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
    ner_entities.setdefault(ent.label_, []).append(ent.text)
for k in ner_entities:
    ner_entities[k] = list(set(ner_entities[k]))

# -----------------------------
# Extraction BERT NER
# -----------------------------
bert_entities_raw = bert_ner(text)
bert_entities = {}
for ent in bert_entities_raw:
    label = ent['entity_group']
    bert_entities.setdefault(label, []).append(ent['word'])
for k in bert_entities:
    bert_entities[k] = list(set(bert_entities[k]))

# -----------------------------
# Fusion finale des IoCs
# -----------------------------
final_iocs = {
    "regex": regex_iocs,
    "ner": ner_entities,
    "bert_ner": bert_entities
}

# -----------------------------
# Sauvegarde JSON final
# -----------------------------
output_path = Path("results/iocs_final_unified.json")
output_path.parent.mkdir(exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_iocs, f, indent=4)

print("Final unified IoCs (with URLs and CVEs) saved to results/iocs_final_unified.json")
