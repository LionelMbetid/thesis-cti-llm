import re
import json
from pathlib import Path

# -----------------------------
# Regex patterns for IoCs
# -----------------------------
REGEX_PATTERNS = {
    "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "domain": r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
}

# -----------------------------
# Load CTI report
# -----------------------------
input_path = Path("data/sample_report.txt")
text = input_path.read_text(encoding="utf-8")

# -----------------------------
# Extract IoCs
# -----------------------------
extracted_iocs = {}

for ioc_type, pattern in REGEX_PATTERNS.items():
    matches = re.findall(pattern, text)
    extracted_iocs[ioc_type] = list(set(matches))

# -----------------------------
# Save results
# -----------------------------
output_path = Path("results/iocs_regex.json")
output_path.parent.mkdir(exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(extracted_iocs, f, indent=4)

print("IoCs extracted using regex:")
for k, v in extracted_iocs.items():
    print(f"{k}: {len(v)} found")
