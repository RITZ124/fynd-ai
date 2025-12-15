import requests
import os
import streamlit as st
OPENROUTER_API_KEY = st.secrets["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"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://fynd-ai-intern-assignment.streamlit.app",
    "X-Title": "Fynd AI Intern Take Home Assignment"
}


def call_llm(prompt):
    if not OPENROUTER_API_KEY:
        return "OPENROUTER_API_KEY not found in Streamlit secrets."

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
            timeout=20
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







