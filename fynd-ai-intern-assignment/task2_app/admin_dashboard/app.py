import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
from collections import Counter

DATA_FILE = "data.json"

st.title("📊 Admin – AI Feedback Triage System")

try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except:
    data = []

if len(data) == 0:
    st.info("No feedback submitted yet.")
    st.stop()

# Sort by priority
data = sorted(data, key=lambda x: x.get("priority_score", 50), reverse=True)


# ---------- ANALYTICS ----------
st.markdown("## 📈 Feedback Analytics")

ratings = [d["rating"] for d in data]
actions = [d["action_category"] for d in data]

st.metric("Total Feedback", len(data))
st.metric("Average Rating", round(sum(ratings) / len(ratings), 2))

st.markdown("### 🧠 Action Distribution")
st.write(Counter(actions))

st.divider()

# ---------- FEEDBACK LIST ----------
st.markdown("## 🚨 Prioritized Feedback")

for entry in data:
    st.subheader(
        f"⭐ {entry['rating']} | Priority: {entry['priority_score']}"
    )

    st.write("🧠 Consistency:", entry.get("consistency", "Not available"))
    st.write("📌 Action:", entry.get("action_category", "Not available"))
    st.write("📝 Reason:", entry.get("action_reason", "Not available"))


    if entry.get("consistency") == "Contradictory Signals":
        st.warning("⚠️ Rating and review sentiment contradict")

    st.divider()
