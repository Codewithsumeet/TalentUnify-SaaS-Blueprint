from io import BytesIO

from docx import Document
from pypdf import PdfReader

from app.exceptions import ValidationException

PDF_MIME_TYPE = "application/pdf"
DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def extract_text(*, file_bytes: bytes, mime_type: str) -> str:
    if mime_type == PDF_MIME_TYPE:
        reader = PdfReader(BytesIO(file_bytes))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        if not text.strip():
            raise ValidationException("Uploaded PDF has no extractable text")
        return text

    if mime_type == DOCX_MIME_TYPE:
        document = Document(BytesIO(file_bytes))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)
        if not text.strip():
            raise ValidationException("Uploaded DOCX has no extractable text")
        return text

    raise ValidationException("Unsupported resume file type")
