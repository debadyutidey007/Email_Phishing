# FlipKart-Style Phishing Simulation
This project is a simulation of a phishing campaign styled to resemble a FlipKart account verification email and login page. It is intended for educational purposes only to demonstrate phishing techniques and raise awareness about cybersecurity risks. Do not use this code for malicious purposes.

# Overview
The script performs the following:
1. Sends a professional-looking phishing email mimicking FlipKart's branding, prompting the recipient to verify their account.
2. Hosts a Flask web server that serves a fake "Verify Your Account" login page with FlipKart's UI/UX, including animations using Anime.js.
3. Captures credentials entered on the login page and logs them to a file (credentials.log).
4. Logs all actions to both the console and a file (phishing_simulation.log).

# Features
(i) *Email Template*: A responsive HTML email with FlipKart branding, including a logo, verification button, privacy policy, and unsubscribe links.
(ii) *Login Page*: A realistic login page with a navbar, gradient background, and animated form fields styled to match FlipKart's design.
(iii) *Logging*: Captures credentials in plain text and logs actions with timestamps.
(iv) *Configuration*: Easily customizable URLs, company name, and server settings.
(v) *Security*: Simulates a phishing attack to educate users about recognizing suspicious emails and websites.

# Prerequisites
i. Python 3.6+
ii. Required Python packages:
	pip install flask smtplib
iii. A Gmail account with an App Password for sending emails (enable 2-Step Verification and generate an App Password in Google Account settings).
iv. Internet connection for serving the Flask app and sending emails.

# Setup
(i) Clone or download the project files.
(ii) Install dependencies:
	pip install -r requirements.txt
(Create a requirements.txt with flask and any other dependencies if needed.)
(iii) Update the configuration variables in the script:
	(a) COMPANY_NAME: Set to "FlipKart" or your desired company name.
 	(b) COMPANY_LOGO_URL, NAV_ICON_URL: URLs for the logo and navbar icon.
  	(c) SUPPORT_URL, PRIVACY_POLICY_URL, UNSUBSCRIBE_URL: Links for the email footer.
   	(d) PHISHING_HOST, PHISHING_PORT: Host and port for the Flask server (default: 127.0.0.1:8081).
(iv) Ensure the Flask server is accessible at the configured PHISHING_BASE_URL.

# Usage
1. Run the script:
   python phishing.py
2. Enter the following when prompted:
   (a) Target email: The recipient's email address (for testing, use your own email).
   (b) Sender email: Your Gmail address.
   (c) Sender's app password: The App Password generated for your Gmail account.
3. The script will:
   (a) Start the Flask server to host the fake login page.
   (b) Send a phishing email to the target email with a link to the login page.
   (c) Log all actions to phishing_simulation.log.
4. When the recipient clicks the link and submits credentials, they are logged to credentials.log.
5. Press Ctrl+C to stop the server.

# Files
(i) phishing_simulation.py: Main script containing the Flask app, email sender, and server logic.
(ii) phishing_simulation.log: Log file for all actions (created automatically).
(iii) credentials.log: Log file for captured credentials (created automatically).

# Example Output

=== FlipKart-Style Verification Email Simulation ===
Target email: test@example.com
Sender email (Gmail): your.email@gmail.com
Sender's app password: ••••••••
✅ Email sent! Click link lands on http://127.0.0.1:8081/?recipient=test%40example.com
Press Ctrl+C to exit.

Security Notes
(i) Ethical Use: This code is for educational and testing purposes only. Unauthorized use to harm others is illegal and unethical.
(ii) Testing: Only test on systems or accounts you own or have explicit permission to test.
(iii) Credentials Storage: Credentials are stored in plain text in credentials.log. Secure or delete this file after testing.
(iv) Server Exposure: The Flask server runs on 127.0.0.1 by default. If exposed publicly, ensure proper security measures.

# Limitations
(i) Gmail's SMTP server is used, requiring an App Password. Other email providers are not supported.
(ii) The Flask server is not designed for production use (no HTTPS, single-threaded).
(iii) The phishing email may be flagged as spam or blocked by email providers.

# Disclaimer
This project is provided for educational purposes only. The author is not responsible for any misuse or damage caused by this code. Use responsibly and comply with all applicable laws and regulations.
