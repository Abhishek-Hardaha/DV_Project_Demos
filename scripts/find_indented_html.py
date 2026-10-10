import os
import re

files_to_check = []
for root, dirs, files in os.walk("."):
    if any(p in root for p in [".git", ".venv", "__pycache__"]):
        continue
    for f in files:
        if f.endswith(".py"):
            files_to_check.append(os.path.join(root, f))

found = []
for fp in files_to_check:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    matches = re.finditer(r'st\.markdown\(\s*(?:f?["\']{3}|f?["\'])(.*?)(?:["\']{3}|["\'])\s*,\s*unsafe_allow_html=True\)', content, re.DOTALL)
    for m in matches:
        snippet = m.group(1)
        for line in snippet.splitlines():
            if re.match(r'^\s{4,}<', line):
                found.append((fp, line.strip()[:60]))
                break

print(f"Total files with indented html in st.markdown: {len(found)}")
for fp, sample in found:
    print(f"  {fp}: {sample}")
