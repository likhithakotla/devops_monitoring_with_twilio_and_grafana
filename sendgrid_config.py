import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")

# Optional: Raise errors if variables are not defined
if not SENDGRID_API_KEY:
    raise ValueError("Missing SENDGRID_API_KEY in environment.")
if not FROM_EMAIL:
    raise ValueError("Missing FROM_EMAIL in environment.")
if not TO_EMAIL:
    raise ValueError("Missing TO_EMAIL in environment.")
