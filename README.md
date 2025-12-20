📰 Daily News Agent

A fully automated daily news intelligence agent that crawls trusted news sources, extracts meaningful content, summarizes it using a local LLM, and emails you only if something important actually happened.

No APIs. No paid services. Fully open-source.

🚀 What This Does

Every day, the agent:

Crawls selected news websites

Extracts high-quality article text

Filters noise and duplicates

Uses a local LLM to decide:

“Nothing worthwhile” OR

A single concise summary paragraph

Sends the result to your email

🧠 Architecture
DeepHarvest (Web Crawler)
        ↓
In-Memory Text Exporter
        ↓
Local LLM (llama.cpp + Phi-2)
        ↓
Email Delivery (Gmail SMTP)

🛠 Tech Stack

Crawler: DeepHarvest (in-memory exporter)

LLM Runtime: llama.cpp

Model: Phi-2 (Q4_K_M GGUF)

Language: Python 3.10+

Email: Gmail SMTP

Deployment: GitHub Actions or local cron

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/Anajrajeev/daily-news-agent
cd daily-news-agent

2️⃣ Install Python dependencies
pip install deepharvest

3️⃣ Build llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
cp build/bin/llama-cli ../
cd ..

4️⃣ Download the LLM model (Git LFS)
git lfs install
git clone https://huggingface.co/TheBloke/phi-2-GGUF
mv phi-2-GGUF/phi-2.Q4_K_M.gguf model.gguf

🔐 Environment Variables

Create environment variables (or GitHub secrets):

GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password


⚠️ Use a Gmail App Password, not your main password.

▶️ Running Locally
python run.py


If no important news is found, no email is sent.

⏱ Automated Daily Execution

This project is designed to run on:

GitHub Actions (recommended)

Local cron jobs

Headless servers

The machine does NOT need to stay on when using GitHub Actions.

🧪 Example Output
NOTHING WORTHWHILE


OR

Global markets reacted sharply after central banks signaled extended high interest rates, while geopolitical tensions escalated following new sanctions and military developments in Eastern Europe and the Middle East.

📁 Project Structure
daily-news-agent/
├── run.py               # Main execution script
├── model.gguf           # LLM model (Git LFS)
├── llama-cli            # llama.cpp binary
├── README.md
└── .github/workflows/   # GitHub Actions

🔍 Customization

Edit news sources in run.py:

SITES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
]

🧠 Why This Exists

Most news aggregators:

Flood you with noise

Repeat the same stories

Push clickbait

This agent:

Thinks first

Speaks only when needed

Runs entirely on your terms

📜 License

Apache 2.0
Use it, modify it, automate it.

✨ Credits

DeepHarvest — intelligent crawling

llama.cpp — local inference

Phi-2 — compact reasoning model
