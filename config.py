import os
import json
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.keras")
DB_PATH = os.path.join(BASE_DIR, "database", "reports.db")
LOG_PATH = os.path.join(BASE_DIR, "reports", "app.log")
EXCEL_REPORTS_DIR = os.path.join(BASE_DIR, "reports", "generated_Excel")
PDF_REPORTS_DIR = os.path.join(BASE_DIR, "reports", "generated_pdf")
UPLOADS_DIR = os.path.join(BASE_DIR, "reports", "uploaded_images")

IMG_SIZE = (224, 224)



TRAIN_DIR = os.path.join(BASE_DIR, "data", "train")
VAL_DIR = os.path.join(BASE_DIR, "data", "val")
TEST_DIR = os.path.join(BASE_DIR, "data", "test")
BATCH_SIZE = 32
EPOCHS = 20
FINE_TUNE_EPOCHS = 10

EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
AUTHORITY_EMAIL = os.getenv("AUTHORITY_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587



