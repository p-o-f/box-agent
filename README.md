# 📄 Box Contract Risk Agent

An autonomous AI agent that reads every contract in a Box folder, analyzes each one for legal and financial risk using Claude with API calls, and writes a structured risk report back to Box: no human in the loop.

Built with the [Box Python SDK](https://github.com/box/box-python-sdk-gen) and [Anthropic Claude](https://www.anthropic.com).
---

## What It Does

1. **Connects to Box** via OAuth 2.0 and reads all PDFs from a specified folder
2. **Sends each contract to Claude** with a structured legal analysis prompt
3. **Extracts key risk data** — auto-renewal clauses, liability caps, termination penalties, expiration dates, and more
4. **Generates a portfolio risk report** ranked by risk score (1–10)
5. **Writes the report back to Box** as a markdown file in the same folder

Just one command. Walk away and come back to a risk report in your Box folder.

---

## Demo (included in this repo)

Given a Box folder with 5 contracts:

```
contracts/
├── contract_01_saas_vendor_agreement.pdf
├── contract_02_nda_expired.pdf
├── contract_03_service_agreement_highrisk.pdf
├── contract_04_software_license_evergreen.pdf
└── contract_05_msa_clean.pdf
```

The agent produces a report like this:
(1x run will cost approx. $0.24 of API credits) 
```
## Portfolio Summary

| Metric          | Value   |
|-----------------|---------|
| Total Contracts | 5       |
| 🔴 High Risk    | 3       |
| 🟡 Medium Risk  | 1       |
| 🟢 Low Risk     | 1       |
| Average Score   | 6.2/10  |
```

Each contract gets a detailed breakdown of flagged clauses with specific recommendations.

---

## Stack

| Component | Tool |
|-----------|------|
| Content layer | [Box](https://box.com) — file storage, retrieval, and report delivery |
| AI analysis | [Anthropic Claude](https://anthropic.com) — PDF understanding + legal reasoning |
| Auth | Box OAuth 2.0 |
| Language | Python 3.11+ |

---

## Setup

### Prerequisites

- Python 3.11+
- A [Box Developer account](https://developer.box.com) with an OAuth 2.0 app
- An [Anthropic API key](https://console.anthropic.com)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/box-contract-agent.git
cd box-contract-agent
```

### 2. Install dependencies

```bash
pip install box-sdk-gen anthropic python-dotenv
```

### 3. Configure Box OAuth app

1. Go to [developer.box.com](https://developer.box.com) → My Apps → Create App
2. Choose **Custom App** → **User Authentication (OAuth 2.0)**
3. Under **Redirect URIs**, add: `http://localhost:8080/callback`
4. Enable scopes: **Read all files and folders** + **Write all files and folders**
5. Copy your **Client ID** and **Client Secret**

### 4. Set up environment variables

```bash
cp example.env .env
```

Fill in your `.env`:

```
BOX_CLIENT_ID=your_client_id_here
BOX_CLIENT_SECRET=your_client_secret_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 5. Upload contracts to Box

Create a folder called `contracts` in your Box account and upload your PDF contracts. Then update the folder ID in `agent.py`:

```python
CONTRACTS_FOLDER_ID = "your_folder_id_here"
```

To find your folder ID, run:

```bash
python list_files.py
```

### 6. Run the agent

```bash
python agent.py
```

A browser window will open for Box OAuth. After authenticating, the agent runs fully autonomously and uploads the report to your Box folder.

---

## Project Structure

```
box-contract-agent/
├── agent.py          # Main agent — fetches, analyzes, reports
├── list_files.py     # Utility to list Box folder contents and IDs
├── auth_test.py      # Standalone Box auth verification script
├── example.env       # Environment variable template
├── .gitignore        # Excludes .env and venv
└── README.md
```

---

## How the Analysis Works

Each contract is sent to Claude as a base64-encoded PDF with a structured system prompt that instructs it to return JSON with:

- Risk level (`LOW / MEDIUM / HIGH`) and score (1–10)
- Flagged clauses with severity, issue description, and recommendation
- Key metadata: parties, dates, contract type
- Plain-English summary

The agent aggregates all results into a portfolio-level report sorted by risk score descending.

---

## Known Limitations & Production Considerations

**OAuth flow requires browser interaction.** The current implementation uses OAuth 2.0 with a local callback server, which requires a human to authenticate in the browser on first run. For fully headless/automated deployments, replace with [Box Client Credentials Grant (CCG)](https://developer.box.com/guides/authentication/client-credentials/) using a service account.

**No token persistence.** Auth tokens are not cached between runs — the browser flow triggers every time. Production deployments should serialize and refresh tokens.

**PDF text extraction.** Claude reads PDFs natively via the Anthropic Files API. Scanned/image-only PDFs without embedded text may produce lower quality analysis.

**Not legal advice.** This tool is for triage and flagging only. Always have qualified legal counsel review contracts before making decisions.

---

## Extending This

Some ideas for taking this further:

- **Slack/email alerts** — notify the team when a high-risk contract is detected
- **Scheduled runs** — use a cron job or Box webhook to trigger on new file uploads
- **Database logging** — persist results to Postgres or similar for trend analysis
- **Multi-folder support** — scan across an entire Box enterprise for contract hygiene
- **CCG auth** — remove the browser dependency for fully automated pipelines

---

## Related

- [Box MCP Server](https://developer.box.com/guides/box-mcp/) — for interactive Claude Desktop + Box workflows
- [Box Python SDK Gen](https://github.com/box/box-python-sdk-gen)
- [Anthropic Claude API Docs](https://docs.anthropic.com)

---

## License

MIT
