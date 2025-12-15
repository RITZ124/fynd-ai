import requests
import os

OPENROUTER_API_KEY = os.getenv("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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_llm(prompt):
    try:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=HEADERS,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"AI service unavailable: {str(e)}"


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
