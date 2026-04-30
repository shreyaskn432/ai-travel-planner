import streamlit as st
from planner import generate_itinerary
import re

st.set_page_config(page_title="AI Travel Planner", layout="wide")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✈️ AI Travel Planner")

# Extract user input
def extract_details(text):
    destination = "Goa"
    days = 3
    budget = "10000"
    interests = text

    day_match = re.search(r'(\d+)\s*day', text.lower())
    if day_match:
        days = int(day_match.group(1))

    budget_match = re.search(r'(\d{4,6})', text)
    if budget_match:
        budget = budget_match.group(1)

    places = ["goa", "manali", "ooty", "bangalore", "delhi", "coorg"]
    for w in text.lower().split():
        if w in places:
            destination = w.capitalize()

    return destination, days, budget, interests


# Card UI function
def display_itinerary(result):
    days = result.split("Day ")

    for d in days:
        if not d.strip():
            continue

        st.markdown(
            f"""
            <div style="background:#1e1e1e;padding:20px;border-radius:12px;margin-bottom:15px">
            <h3 style="color:#4CAF50;">Day {d[:1]}</h3>
            <p style="font-size:16px;line-height:1.6">{d[2:]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# Input
user_input = st.chat_input("Describe your trip...")

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    destination, days, budget, interests = extract_details(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            result = generate_itinerary(destination, days, budget, interests)

            display_itinerary(result)

    st.session_state.messages.append({"role": "assistant", "content": result})