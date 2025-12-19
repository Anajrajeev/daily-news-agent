import os
import asyncio
import subprocess
import smtplib
from email.mime.text import MIMEText

from deepharvest import DeepHarvest, CrawlConfig

# ---------- CONFIG ----------
SITES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
]

MODEL_PATH = "model.gguf"
LLAMA_BIN = "./llama"

# ---------- CRAWL FUNCTION ----------
async def crawl_sites():
    texts = []

    for site in SITES:
        try:
            config = CrawlConfig(
                seed_urls=[site],
                max_depth=0,          # homepage only
                enable_js=False,       # faster + stable
                max_urls=5,
            )

            crawler = DeepHarvest(config)
            await crawler.initialize()
            await crawler.crawl()

            for page in crawler.storage.pages.values():
                if page.content:
                    texts.append(page.content)

            await crawler.shutdown()

        except Exception as e:
            print(f"Failed to crawl {site}: {e}")

    return "\n\n".join(texts)

# ---------- MAIN ----------
async def main():
    content = await crawl_sites()

    if not content.strip():
        content = "No significant news content found."

    prompt = f"""
Scan the following news content.

If nothing important happened, reply EXACTLY with:
NOTHING WORTHWHILE

Otherwise, summarize all important events into ONE concise paragraph.

CONTENT:
{content[:12000]}
"""

    result = subprocess.check_output(
        [
            LLAMA_BIN,
            "-m", MODEL_PATH,
            "-p", prompt,
            "-n", "256",
            "--ctx-size", "2048",
            "--temp", "0.2",
        ],
        stderr=subprocess.STDOUT,
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

# ---------- RUN ----------
if __name__ == "__main__":
    asyncio.run(main())
