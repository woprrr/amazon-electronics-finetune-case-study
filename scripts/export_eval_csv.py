#!/usr/bin/env python3
import csv, json, sys
in_path = sys.argv[1] if len(sys.argv) > 1 else "src/prompt_sets/eval_inquiries.json"
prompts = json.load(open(in_path))
w = csv.writer(sys.stdout)
w.writerow(["inquiry","model","answer","tokens_out","latency_ms","exactitude","actionnabilite","exhaustivite","securite","score_pondere"])
for p in prompts:
    w.writerow([p,"","","","","","","","",""])
