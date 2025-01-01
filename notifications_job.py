import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import schedule
import smtplib

# Store the links globally
links_list = []

# Function to check for updates
def check_updates():
    global links_list
    for link in links_list:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Logic to find job notifications (customize based on the website's HTML structure)
                job_posts = soup.find_all('a', string="Jobs")  # Adjust based on actual content
                if job_posts:
                    send_email(link, "New job notification found!", str(job_posts))
            else:
                print(f"Error fetching {link}: Status Code {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

# Function to send email
def send_email(link, subject, content):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    recipient_email = "recipient_email@gmail.com"

    message = f"Subject: {subject}\n\nNew updates on {link}:\n{content}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message)
        print(f"Email sent for updates on {link}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Streamlit UI
st.title("Job Notification Tracker")
st.header("Add websites to track job notifications")

# Initialize session state for storing links
if 'links' not in st.session_state:
    st.session_state['links'] = []

# User input for websites
with st.form("add_link"):
    link = st.text_input("Enter website link")
    add_button = st.form_submit_button("Add Link")

    if add_button and link:
        st.session_state['links'].append(link)
        st.success(f"Added: {link}")

# Display tracked websites
st.write("### Tracked Websites:")
st.write(st.session_state['links'])

# Update global links list
links_list = st.session_state['links']

# Schedule the scraper every hour
if links_list:
    schedule.every(1).hours.do(check_updates)

# Run the schedule in a loop (use Streamlit's button to start the loop)
if st.button("Start Tracking"):
    st.write("Tracking job notifications... Leave the app running for real-time updates.")
    while True:
        schedule.run_pending()
        time.sleep(1)
