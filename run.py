from deepharvest import extract
import subprocess

SITES = [
    "https://example.com",
    "https://example2.com"
]

texts = []
for site in SITES:
    texts.append(extract(site)["text"])

content = "\n".join(texts)

prompt = f"""
Scan the content.
If nothing important happened, reply exactly:
NOTHING WORTHWHILE

Else summarize everything in one paragraph.
Content:
{content}
"""

# Call llama.cpp model
result = subprocess.check_output([
    "./llama",
    "-m", "model.gguf",
    "-p", prompt,
    "-n", "200"
])

print(result.decode())
