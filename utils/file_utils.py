import os
import uuid
from datetime import datetime

from PIL import Image

from config import UPLOADS_DIR

os.makedirs(UPLOADS_DIR, exist_ok=True)


def generate_unique_filename(extension: str = "jpg") -> str:
    """e.g. '20260803_011530_4a1b9c.jpg' -- sortable by time, unique per report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    return f"{timestamp}_{unique_id}.{extension}"


def save_uploaded_image(image: Image.Image) -> str:
    """Saves a PIL image into UPLOADS_DIR and returns the full path."""
    filename = generate_unique_filename()
    path = os.path.join(UPLOADS_DIR, filename)
    image.convert("RGB").save(path, format="JPEG")
    return path