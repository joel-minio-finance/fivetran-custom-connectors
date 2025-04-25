import os

ACCOUNT_ID = os.getenv("LEADFEEDER_ACCOUNT_ID")
BASE_API_URL = os.getenv("LEADFEEDER_BASE_API_URL")

VISIT_API = f"accounts/{ACCOUNT_ID}/visits"
LEAD_API = f"accounts/{ACCOUNT_ID}/leads"
