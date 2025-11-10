#!/usr/bin/env python3
import os
import time
import json
import argparse
import csv
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FT_MODEL_ID = os.getenv("FT_MODEL_ID", "ft:gpt-4.1-mini-2025-04-14:buldee:amazon-electronics-ft:CaOkOuOd")
BASELINE_MODEL_ID = os.getenv("BASELINE_MODEL_ID", "gpt-4.1-mini-2025-04-14")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
SEED = int(os.getenv("SEED", "42"))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "300"))

def call_model(model, inquiry):
    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "input": [
            {"role":"system","content":"You are a helpful Amazon customer support assistant. Answer factually, concisely, and safely. Do not expose internal processes. For policy or availability details that vary by region or account, instruct the user to check 'Your Orders' or the checkout flow."},
            {"role":"user","content": f'Inquiry: "{inquiry}"'}
        ],
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS
    }
    t0 = time.time()
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    latency = int((time.time()-t0)*1000)
    r.raise_for_status()
    data = r.json()
    ans = None
    try:
        ans = data["output"][0]["content"][0]["text"]
    except Exception:
        try:
            ans = data["content"][0]["text"]
        except Exception:
            ans = json.dumps(data)[:2000]
    return ans, latency

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts", default="src/prompt_sets/eval_inquiries.json")
    ap.add_argument("--out", default="reports/eval_results.csv")
    args = ap.parse_args()

    if not OPENAI_API_KEY:
        raise SystemExit("OPENAI_API_KEY manquant.")

    prompts = json.load(open(args.prompts, "r", encoding="utf-8"))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["inquiry","model","answer","latency_ms","exactitude","actionnabilite","exhaustivite","securite","score_pondere"])
        for p in prompts:
            for model in (FT_MODEL_ID, BASELINE_MODEL_ID):
                ans, lat = call_model(model, p)
                w.writerow([p, model, ans, lat, "", "", "", "", ""])

if __name__ == "__main__":
    main()
