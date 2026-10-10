import re

s = """
        <div class="gallery-card">
            <h4>Title</h4>
            <p>Description</p>
        </div>
"""

cleaned = re.sub(r'^[ \t]+', '', s, flags=re.MULTILINE).strip()
print("Cleaned output:")
print(repr(cleaned))
print("Each line starts with:")
for line in cleaned.splitlines():
    print("  Line:", repr(line[:15]))
