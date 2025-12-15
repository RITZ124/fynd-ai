# -*- coding: utf-8 -*-
import requests
import os
import streamlit as st
import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/devstral-2512:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "Referer": "https://fynd-ai.streamlit.app",
    "X-Title": "Fynd AI Intern Assignment",
    "User-Agent": "fynd-ai-intern/1.0"
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
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI service unavailable: {str(e)}"


def analyze_feedback(review, rating):
    prompt = f"""
You are an internal business feedback analysis system.

Rating: {rating}
Review: "{review}"

Return ONLY valid JSON in this exact format:

{{
  "consistency": "Consistent Positive | Consistent Negative | Contradictory Signals | Ambiguous",
  "action_category": "Apology & Recovery | Refund / Escalation | Feature Improvement | Staff Training | Marketing Opportunity | No Action Needed",
  "action_reason": "short explanation",
  "priority_score": 0
}}

Rules:
- Low rating and negative sentiment means high priority.
- Positive feedback means low priority.
- Contradictory signals means medium priority.
"""
    return call_llm(prompt)
