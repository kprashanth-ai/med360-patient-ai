import os
from app.config import settings


def save_upload(filename: str, contents: bytes) -> str:
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    return file_path


def delete_upload(filename: str):
    file_path = os.path.join(settings.upload_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
