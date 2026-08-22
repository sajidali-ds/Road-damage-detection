import io
from PIL import Image


def load_image_from_path(path: str) -> Image.Image:
    return Image.open(path)


def load_image_from_bytes(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))


def load_image_from_uploaded_file(uploaded_file) -> Image.Image:
    """uploaded_file is a Streamlit UploadedFile object from st.file_uploader()."""
    return Image.open(uploaded_file)
