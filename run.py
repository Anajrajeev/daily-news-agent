import asyncio
import os
import subprocess
import smtplib
from email.mime.text import MIMEText

from deepharvest import DeepHarvest, CrawlConfig


# ---------------- CONFIG ----------------
SITES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
]

MODEL_PATH = "model.gguf"
LLAMA_BIN = "./llama-cli"  # built from llama.cpp

MAX_CHARS = 12000


# ---------------- CRAWL ----------------
async def crawl_sites():
    config = CrawlConfig(
        seed_urls=SITES,
        max_depth=0,
        enable_js=False,
        exporters=["memory"],   # 🔑 NEW FEATURE
    )

    crawler = DeepHarvest(config)
    await crawler.initialize()
    await crawler.crawl()
    await crawler.shutdown()

    texts = crawler.exporters["memory"].texts
    return "\n\n".join(texts)


# ---------------- LLM ----------------
def run_llm(text: str) -> str:
    if not text.strip():
        return "NOTHING WORTHWHILE"

    prompt = f"""
Scan the following news content.

If nothing important happened, reply EXACTLY with:
NOTHING WORTHWHILE

Otherwise, summarize all important events into ONE concise paragraph.

CONTENT:
{text[:MAX_CHARS]}
"""

    result = subprocess.run(
        [
            LLAMA_BIN,
            "-m", MODEL_PATH,
            "-p", prompt,
            "-n", "256",
            "--ctx-size", "2048",
            "--temp", "0.2",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


# ---------------- EMAIL ----------------
def send_email(body: str):
    EMAIL_FROM = os.getenv("GMAIL_USER")
    EMAIL_PASS = os.getenv("GMAIL_PASS")
    EMAIL_TO = EMAIL_FROM

    if not EMAIL_FROM or not EMAIL_PASS:
        print("⚠️ Email credentials missing, skipping email.")
        print(body)
        return

    msg = MIMEText(body)
    msg["Subject"] = "Daily News Summary"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

    print("📧 Email sent successfully.")


# ---------------- MAIN ----------------
async def main():
    print("🕷 Crawling news sites...")
    content = await crawl_sites()

    if not content.strip():
        print("📰 No meaningful content found.")
        return

    print("🧠 Running LLM...")
    summary = run_llm(content)

    print("✉️ Sending email...")
    send_email(summary)


if __name__ == "__main__":
    asyncio.run(main())
