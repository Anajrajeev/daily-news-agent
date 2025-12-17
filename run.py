import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from deepharvest import extract

# ---------- CONFIG ----------
SITES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
]

MODEL_PATH = "model.gguf"
LLAMA_BIN = "./llama"

# ---------- EXTRACT CONTENT ----------
texts = []
for site in SITES:
    try:
        data = extract(site)
        texts.append(data.get("text", ""))
    except Exception as e:
        print(f"Failed to extract {site}: {e}")

content = "\n\n".join(texts)

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
result = subprocess.check_output([
    LLAMA_BIN,
    "-m", MODEL_PATH,
    "-p", prompt,
    "-n", "200",
    "--temp", "0.2"
])

output = result.decode().strip()

# ---------- EMAIL ----------
EMAIL_FROM = os.getenv("GMAIL_USER")
EMAIL_TO = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_PASS")

msg = MIMEText(output)
msg["Subject"] = "Daily News Summary"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.send_message(msg)

print("Email sent successfully.")
