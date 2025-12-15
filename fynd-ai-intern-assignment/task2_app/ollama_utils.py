import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def call_llm(prompt):
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=8)
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception:
        return "AI service unavailable (local LLM not running)."


def analyze_feedback(review, rating):
    prompt = f"""
You are an internal AI system for business feedback analysis.

Rating: {rating}
Review: "{review}"

Return ONLY valid JSON in this format:

{{
  "consistency": one of [
    "Consistent Positive",
    "Consistent Negative",
    "Contradictory Signals",
    "Ambiguous"
  ],
  "action_category": one of [
    "Apology & Recovery",
    "Refund / Escalation",
    "Feature Improvement",
    "Staff Training",
    "Marketing Opportunity",
    "No Action Needed"
  ],
  "action_reason": "short explanation",
  "priority_score": integer between 0 and 100
}}

Guidelines:
- Low rating + negative tone → high priority
- Positive feedback → low priority
- Contradictory signals → medium priority
"""
    return call_llm(prompt)
