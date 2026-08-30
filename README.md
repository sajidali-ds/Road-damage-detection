# 🛣️ Road Damage Detection

A Streamlit web app that classifies road-related civic issues from an uploaded photo using an **EfficientNet** image classifier, tags the issue with its **GPS location**, and lets you report it to the concerned authority — via **email**, or as a downloadable **PDF/Excel report**. All submitted reports are logged and viewable in a history tab.

---

## ✨ Features

- 📤 **Upload a road image** (JPG/JPEG/PNG) and get an instant prediction
- 🧠 **7-class EfficientNet classifier** with per-class confidence scores
- 📍 **Location tagging** — enter latitude/longitude, get a reverse-geocoded address + Google Maps link
- 📨 **Email the report** directly to the concerned authority
- 📄 **Generate PDF & Excel reports** for offline records
- 📋 **Report history** — view all previously submitted reports with status
- 🗃️ Reports are persisted in a local SQLite database

## 🏷️ Detected Classes

The model classifies an uploaded image into one of the following 7 categories:

1. Broken Road Sign Issues
2. Damaged Road Issues
3. Illegal Parking Issues
4. Littering / Garbage on Public Places Issues
5. Mixed Issues
6. Pothole Issues
7. Vandalism Issues

## 🧱 Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Model | TensorFlow / Keras (EfficientNet) |
| Image handling | Pillow |
| Reports | fpdf2 (PDF), openpyxl (Excel) |
| Storage | SQLite |
| Geolocation | Reverse geocoding + Google Maps link |
| Email | SMTP (Gmail) |

## 📂 Project Structure

```
Road-damage-detection/
├── Training/            # Model training scripts/notebooks
├── data/                 # Dataset (train/val/test splits)
├── database/             # SQLite DB (reports.db)
├── deployment/           # Deployment-related files
├── models/                # Trained model (best_model.keras)
├── preprocessing/        # Data preprocessing scripts
├── reports/               # Generated PDFs, Excel files, uploaded images, logs
├── test/                  # Tests
├── utils/                 # Helper modules (db, email, maps, geolocation, PDF/Excel gen, logger)
├── app.py                 # Streamlit app entry point
├── config.py              # Paths, class names, email & API config
├── predict.py              # Inference logic
└── requirements.txt
```

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sajidali-ds/Road-damage-detection.git
   cd Road-damage-detection
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install python-dotenv
   ```

4. **Add the trained model and class names**
   Place the following inside `models/`:
   - `best_model.keras` — the trained EfficientNet model (see `config.py` → `MODEL_PATH`)
   - `class_names.json` — a JSON array of the 7 class names, in the same order used during training:
     ```json
     [
       "Broken Road Sign Issues",
       "Damaged Road issues",
       "Illegal Parking Issues",
       "Littering Garbage on Public Places Issues",
       "Mixed Issues",
       "Pothole Issues",
       "Vandalism Issues"
     ]
     ```

5. **Create a `.env` file** in the project root (never commit this file — see Security note below):
   ```
   EMAIL_ENABLED=false
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_16_char_app_password
   AUTHORITY_EMAIL=authority_email@gmail.com
   GOOGLE_MAPS_API_KEY=
   ```
   - `EMAIL_ENABLED` defaults to `false` so the app runs safely even if no `.env` is present.
   - Set it to `true` and fill in `SENDER_EMAIL`/`SENDER_PASSWORD` (a Gmail **App Password**, not your regular password) once you want email reporting to work.
   - `config.py` loads these via `python-dotenv`'s `load_dotenv()`.

6. **Run the app**
   ```bash
   streamlit run app.py
   ```
   > Restart the app (stop with `Ctrl+C` and re-run) after any change to `.env` — Streamlit's hot-reload does not re-trigger `load_dotenv()`.

## 🚀 Usage

1. Open the app in your browser (Streamlit will give you a local URL).
2. Go to the **"New Report"** tab → upload a road/civic issue photo.
3. View the predicted class and confidence breakdown.
4. Enter/confirm the **latitude & longitude** of the issue location.
5. Either:
   - Click **"Report to authority"** to email the report, or
   - Click **"Generate PDF + Excel"** to download the report files.
6. Check the **"Report History"** tab to see all past submissions.

## 🔐 Security Note

Secrets (`SENDER_EMAIL`, `SENDER_PASSWORD`, `AUTHORITY_EMAIL`, `GOOGLE_MAPS_API_KEY`) are now loaded from a local `.env` file via `python-dotenv`, instead of being hardcoded in `config.py`. Make sure:

- `.env` is listed in `.gitignore` and is **never committed**.
- If you ever had an earlier version of this repo with hardcoded credentials, treat that password as compromised — rotate/revoke it from your email provider's app-password settings, since removing it from the latest commit does not remove it from Git history.

## 🧪 Model Training

Training scripts/notebooks live in the `Training/` folder. Model input size is `224x224`, trained with configurable `BATCH_SIZE`, `EPOCHS`, and `FINE_TUNE_EPOCHS` (see `config.py`).

## 📌 Requirements

```
tensorflow
keras
streamlit
numpy
pillow
scikit-learn
matplotlib
pandas
split-folders
requests
openpyxl
fpdf2
pytest
```

## 🤝 Contributing

Issues and pull requests are welcome. Please open an issue first to discuss significant changes.
