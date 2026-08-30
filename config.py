import os
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


CLASS_NAMES = [
    "Broken Road Sign Issues",
    "Damaged Road issues",
    "Illegal Parking Issues",
    "Littering Garbage on Public Places Issues",
    "Mixed Issues",
    "Pothole Issues",
    "Vandalism Issues",
]

TRAIN_DIR = "/content/drive/MyDrive/Road_damage_cnn_project/CNN_Road_Data/split_data/train"
VAL_DIR = "/content/drive/MyDrive/Road_damage_cnn_project/CNN_Road_Data/split_data/val"
TEST_DIR = "/content/drive/MyDrive/Road_damage_cnn_project/CNN_Road_Data/split_data/test"
BATCH_SIZE = 32
EPOCHS = 20
FINE_TUNE_EPOCHS = 10

EMAIL_ENABLED = True
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
AUTHORITY_EMAIL = os.getenv("AUTHORITY_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


GOOGLE_MAPS_API_KEY = ""
