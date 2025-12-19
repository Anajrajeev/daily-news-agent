import os
import subprocess
import smtplib
from email.mime.text import MIMEText

from deepharvest.core.harvester import Harvester

# ---------- CONFIG ----------
SITES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
]

MODEL_PATH = "model.gguf"
LLAMA_BIN = "./llama"

# ---------- EXTRACT CONTENT ----------
harvester = Harvester()

texts = []
for site in SITES:
    try:
        docs = harvester.harvest([site])
        for doc in docs:
            if isinstance(doc, dict) and "content" in doc:
                texts.append(doc["content"])
    except Exception as e:
        print(f"Failed to extract {site}: {e}")

content = "\n\n".join(texts)

if not content.strip():
    content = "No news content extracted."

# ---------- PROMPT ----------
prompt = f"""
Scan the following news content.

If nothing important happened, reply EXACTLY with:
NOTHING WORTHWHILE

Otherwise, summarize all important events into ONE concise paragraph.

CONTENT:
{content[:12000]}
"""

# ---------- RUN LLM ----------
result = subprocess.check_output(
    [
        LLAMA_BIN,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "256",
        "--ctx-size", "2048",
        "--temp", "0.2"
    ],
    stderr=subprocess.STDOUT
)

output = result.decode(errors="ignore").strip()

# ---------- EMAIL ----------
EMAIL_FROM = os.getenv("GMAIL_USER")
EMAIL_TO = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_PASS")

if not EMAIL_FROM or not EMAIL_PASS:
    raise RuntimeError("GMAIL_USER or GMAIL_PASS not set")

msg = MIMEText(output)
msg["Subject"] = "Daily News Summary"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.send_message(msg)

print("Email sent successfully.")
