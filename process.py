from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()  + "\n"

    print(f"Extracted {len(text)} characters\n")
    return text

def split_text(text: str) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )

    all_splits = text_splitter.split_text(text)

    print(f"Split text into {len(all_splits)} chunks\n")
    return all_splits

