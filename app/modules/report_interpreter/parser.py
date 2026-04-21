import base64
from pathlib import Path

_MAX_VISION_PAGES = 10


class ImageBasedPDFError(Exception):
    pass


def extract_text(file_path: str, content_type: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Report file not found: {file_path}")

    if "pdf" in content_type or path.suffix.lower() == ".pdf":
        return _extract_pdf(file_path)

    if "image" in content_type or path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        raise NotImplementedError("Image reports not supported yet — please upload a PDF.")

    return path.read_text(encoding="utf-8", errors="ignore")


def extract_images_from_pdf(file_path: str) -> list[str]:
    """Render each PDF page to a base64 PNG (max _MAX_VISION_PAGES pages)."""
    import fitz  # pymupdf
    doc = fitz.open(file_path)
    images = []
    for page in doc.pages(0, min(len(doc), _MAX_VISION_PAGES)):
        pix = page.get_pixmap(dpi=150)
        images.append(base64.b64encode(pix.tobytes("png")).decode())
    return images


def _extract_pdf(file_path: str) -> str:
    import pdfplumber
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    full_text = "\n\n".join(pages)
    if not full_text.strip():
        raise ImageBasedPDFError("PDF contains no selectable text — rendering pages for vision extraction.")
    return full_text
