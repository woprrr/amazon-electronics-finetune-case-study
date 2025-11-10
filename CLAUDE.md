# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a case study demonstrating the value of fine-tuning GPT-4.1-mini for Amazon Electronics customer support. The repository enables comparison between baseline and fine-tuned model responses.

**Fine-tuned Model:**
- ID: `ft:gpt-4.1-mini-2025-04-14:buldee:amazon-electronics-ft:CaOkOuOd`
- Base: `gpt-4.1-mini-2025-04-14`
- Training: 33,978 tokens across 3 epochs
- Status: Private (add reviewers to OpenAI org if needed)

## Environment Setup

1. Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`
2. Create virtual environment: `python3 -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies (if requirements.txt exists): `pip install -r requirements.txt`

Required environment variables:
- `OPENAI_API_KEY`: Required for all API calls
- `FT_MODEL_ID`: Fine-tuned model ID (defaults to project model)
- `BASELINE_MODEL_ID`: Baseline model ID (defaults to gpt-4.1-mini-2025-04-14)
- `TEMPERATURE`: Model temperature (default: 0.2)
- `SEED`: Random seed (default: 42)
- `MAX_OUTPUT_TOKENS`: Response limit (default: 300)

## Running Evaluations

**Quick test with curl scripts:**
```bash
# Test fine-tuned model
./scripts/curl_call_ft.sh "What is the return policy for electronics?"

# Test baseline model
./scripts/curl_call_baseline.sh "How do I track my order?"
```

**Full evaluation run:**
```bash
python src/evaluate.py --prompts src/prompt_sets/eval_inquiries.json --out reports/eval_results.csv
```

This generates `reports/eval_results.csv` with columns ready for manual scoring:
- inquiry, model, answer, latency_ms
- exactitude (0.4 weight), actionnabilite (0.25), exhaustivite (0.25), securite (0.10)
- score_pondere (calculated after manual scoring)

**Generate blank evaluation template:**
```bash
python scripts/export_eval_csv.py src/prompt_sets/eval_inquiries.json > template.csv
```

## Architecture

**Data Format:**
- Training/validation data in `data/` directory as JSONL files
- OpenAI `messages` format with system/user roles
- Tone: factual, concise, safe

**System Prompt:**
All model calls use: "You are a helpful Amazon customer support assistant. Answer factually, concisely, and safely."

**API Endpoint:**
This project uses `https://api.openai.com/v1/responses` (not the standard `/chat/completions` endpoint). Requests use `input` field (array of messages) instead of `messages`.

**Evaluation Scoring:**
- Manual 1-5 scale per criterion
- Weighted score: Exactitude (40%) + Actionnabilité (25%) + Exhaustivité (25%) + Sécurité/Ton (10%)
- Run `src/evaluate.py` to get raw responses, then manually score in CSV

**Test Inquiries:**
Located in `src/prompt_sets/eval_inquiries.json` - covers return policies, order tracking, technical specs (4K120/VRR, eSIM), troubleshooting, and OS updates.

## Security

- Never commit API keys or `.env` files to git
- The fine-tuned model is private; coordinate access through OpenAI organization
- See `SECURITY.md` for vulnerability reporting
