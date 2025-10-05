# === Environment Variables ===
# SENDER_EMAIL = #SENDER_EMAIL
# APP_PASSWORD = #APP_PASSWORD
# RECIPIENT_EMAIL = #RECIPIENT_EMAIL
# BACKEND_INFER_URL = http://backend:8000/infer
# ALERT_TIME = 09:00

import os
import datetime
import time
import schedule
import requests
import yagmail
from dotenv import load_dotenv

# === Load environment variables from .env ===
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
BACKEND_URL = os.getenv("BACKEND_INFER_URL", "http://backend:8000/infer")
ALERT_TIME = os.getenv("ALERT_TIME", "09:00")

print("alert_service.py loaded successfully.")
print(f"SENDER_EMAIL: {SENDER_EMAIL}")
print(f"BACKEND_URL: {BACKEND_URL}")
print(f"ALERT_TIME: {ALERT_TIME}")


def run_infer_and_notify():
    """
    Runs the backend inference endpoint and sends an email alert
    if any extreme stock events or AI-based recommendations are found.
    """
    print("Running run_infer_and_notify()...", flush=True)
    try:
        print(f"Connecting to backend at {BACKEND_URL}", flush=True)
        res = requests.get(BACKEND_URL, timeout=30)
        res.raise_for_status()
        data = res.json()

        results = [r for r in data.get("results", []) if r.get("extreme_alerts")]
        print(f"Backend returned {len(results)} results.", flush=True)

        # No alerts for today
        if not results:
            print("No extreme alerts today.")
            return

        # Prepare email content
        today = datetime.date.today().strftime("%Y-%m-%d")
        subject = f"Stock AI Alerts - {today}"
        body_lines = []

        for item in results:
            ticker = item.get("ticker", "Unknown")
            body_lines.append(f"Ticker: {ticker}")

            # Add detected extreme events
            for alert in item.get("extreme_alerts", []):
                body_lines.append(f"  - {alert}")

            # Add AI suggestion
            if item.get("ai_suggestion"):
                body_lines.append(f"AI Suggestion: {item['ai_suggestion']}")
            body_lines.append("")

        body = "\n".join(body_lines)

        print("Preparing to send email...", flush=True)

        # Send email notification
        yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
        yag.send(to=RECIPIENT_EMAIL, subject=subject, contents=body)
        print(f"Email sent successfully: {subject}", flush=True)

    except Exception as e:
        print(f"Error in alert service: {e}", flush=True)


# === Schedule job ===
schedule.every().day.at(ALERT_TIME).do(run_infer_and_notify)

print(f"Alert service started. Scheduled daily at {ALERT_TIME}.", flush=True)

# === Run once immediately for testing ===
print("Running immediate test execution...", flush=True)
run_infer_and_notify()

# === Keep service running ===
while True:
    schedule.run_pending()
    time.sleep(60)
