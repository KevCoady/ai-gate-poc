#!/usr/bin/env python3
import os
import subprocess
import sys
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("\n[ERROR] OPENAI_API_KEY environment variable is missing.", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

def get_git_diff():
    # Ignore virtualenvs, lockfiles, and bytecode caches
    ignore = [":(exclude)*venv*", ":(exclude)*lock*", ":(exclude)__pycache__*"]
    cmd = ["git", "diff", "origin/main...HEAD", "--"] + ignore
    try:
        return subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Git diff error: {e}", file=sys.stderr)
        sys.exit(1)

diff = get_git_diff().strip()

if not diff:
    print("[PASS] No diff found against origin/main. Nothing to review.")
    sys.exit(0)

# Avoid raw triple-backtick collision by using string concatenation or alternative delimiters
prompt = (
    "You are an uncompromising code gatekeeper inspecting code changes before a Pull Request can be opened.\n"
    "Analyze this diff strictly for:\n"
    "1. Security vulnerabilities (SQL Injection, XSS, unauthenticated endpoints, exposed credentials).\n"
    "2. Bug regressions, unhandled exceptions, and edge cases.\n"
    "3. Code quality and correctness.\n\n"
    "Git Diff:\n"
    + diff[:25000]
    + "\n\nRules:\n"
    "- Line 1 MUST be strictly either '[VERDICT: PASS]' or '[VERDICT: FAIL]'.\n"
    "- Under the verdict, provide a clear, numbered list of issues found and exact fixes required."
)

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}],
)

result = response.choices[0].message.content.strip()

print("\n" + "=" * 50)
print("CODEX QUALITY & SECURITY GATE")
print("=" * 50)
print(result)
print("=" * 50 + "\n")

if "[VERDICT: FAIL]" in result:
    print("❌ Gate failed. Fix the issues before attempting to open a PR.")
    sys.exit(1)
elif "[VERDICT: PASS]" in result:
    print("✅ Gate passed. Code is clean and approved for PR creation.")
    sys.exit(0)
else:
    print("⚠️ Ambiguous verdict returned. Aborting.")
    sys.exit(1)