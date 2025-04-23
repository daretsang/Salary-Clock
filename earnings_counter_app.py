import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)

client = gspread.authorize(creds)

sheet = client.open("EarningsTracker").sheet1

# title
st.title("Live Earnings Counter 💰")

# --- User Input ---
username = st.text_input("Enter your username:")
hourly_wage = st.number_input("Enter your hourly wage ($)", min_value=0.0, step=0.1)

start = st.button("Start Counter")
placeholder = st.empty()

def find_user(username):
    try:
        records = sheet.get_all_records()
        for i, row in enumerate(records):
            if row['username'] == username:
                return i + 2, row  # Sheet rows start at 1, plus header
    except:
        return None, None
    return None, None

if start and username:
    row_index, data = find_user(username)

    if data:
        earned = float(data['earned'])
        hourly_wage = float(data['hourly_wage'])
        st.info(f"Welcome back {username}. You have previously earned ${earned:.2f}")
    else:
        earned = 0.0
        sheet.append_row([username, hourly_wage, earned, datetime.now().isoformat()])
        row_index, _ = find_user(username)
        st.success(f"New user {username} started")

    per_second = hourly_wage / 3600

    # Start live earnings
    update_interval = 30  # seconds
    last_save_time = time.time()

    while True:
        earned += per_second
        placeholder.markdown(f"### You've earned: **${earned:.2f}**")

        # update entire sheet every 30 seconds
        if time.time() - last_save_time > update_interval:
            sheet.batch_update([
                {
                    'range': f'C{row_index}',  # earned
                    'values': [[earned]]
                },
                {
                    'range': f'D{row_index}',  # last_updated
                    'values': [[datetime.now().isoformat()]]
                }
            ])
            last_save_time = time.time()

        time.sleep(1)