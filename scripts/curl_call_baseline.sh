#!/usr/bin/env bash
set -euo pipefail
: "${OPENAI_API_KEY:?Missing OPENAI_API_KEY}"
MODEL_ID="${BASELINE_MODEL_ID:-gpt-4.1-mini-2025-04-14}"
INQUIRY="${1:-What is the return policy for electronics?}"

curl https://api.openai.com/v1/responses           -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json"           -d "{
    \"model\": \"$MODEL_ID\",
    \"input\": [
      {\"role\": \"system\", \"content\": \"You are a helpful Amazon customer support assistant. Answer factually, concisely, and safely. Do not expose internal processes. For policy or availability details that vary by region or account, instruct the user to check 'Your Orders' or the checkout flow.\"},
      {\"role\": \"user\", \"content\": \"Inquiry: \\\"$INQUIRY\\\"\"}
    ],
    \"temperature\": 0.2,
    \"max_output_tokens\": 300
  }"
