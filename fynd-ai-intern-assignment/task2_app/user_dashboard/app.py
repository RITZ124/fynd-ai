import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
from datetime import datetime
from ollama_utils import call_llm, analyze_feedback

DATA_FILE = "data.json"

st.title("📝 Customer Feedback")

rating = st.slider("Select Rating", 1, 5, 3)
review = st.text_area("Write your review")

if st.button("Submit"):
    if review.strip() == "":
        st.error("Review cannot be empty")
    else:
        user_prompt = f"""
You are a professional customer support assistant.

Instructions:
- Be polite and empathetic.
- Acknowledge both rating and review.
- If rating and sentiment mismatch, politely ask for clarification.
- Keep response concise.

Rating: {rating}
Review: {review}
"""
        ai_response = call_llm(user_prompt)

        analysis_raw = analyze_feedback(review, rating)
        try:
            analysis = json.loads(analysis_raw)
        except:
            analysis = {
                "consistency": "Ambiguous",
                "action_category": "No Action Needed",
                "action_reason": "Parsing failed",
                "priority_score": 50
            }

        entry = {
            "rating": rating,
            "review": review,
            "ai_response": ai_response,
            "consistency": analysis["consistency"],
            "action_category": analysis["action_category"],
            "action_reason": analysis["action_reason"],
            "priority_score": analysis["priority_score"],
            "timestamp": str(datetime.now())
        }

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

        st.success("Feedback submitted successfully!")
        st.subheader("AI Response")
        st.write(ai_response)
