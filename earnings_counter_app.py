import streamlit as st
import time

st.title("Live Earnings Counter 💰")

# Input: Hourly wage
hourly_wage = st.number_input("Enter your hourly wage ($)", min_value=0.0, step=0.1)

# Start button
start = st.button("Start Counter")

# Earnings display
placeholder = st.empty()

if start and hourly_wage > 0:
    st.success("Counter running... (leave the page open)")
    per_second = hourly_wage / 3600
    earned = 0.0

    # Run the counter for as long as the user stays on the page
    while True:
        earned += per_second
        placeholder.markdown(f"### You've earned: **${earned:.2f}**")
        time.sleep(1)