import requests
import os
import streamlit as st
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3-8b-instruct:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "Referer": "https://fynd-ai-intern-assignment.streamlit.app",
    "X-Title": "Fynd AI Intern Take Home Assignment",
    "User-Agent": "Fynd-ai-intern-assignment/1.0"
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
            timeout=30
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














