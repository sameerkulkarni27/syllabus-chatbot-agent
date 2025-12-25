from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_path): 
    """Extract text from PDF file"""

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()  + "\n"

    print(f"Extracted {len(text)} characters\n")
    return text

def split_text(text): 
    """Split the text into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,  
        chunk_overlap=CHUNK_OVERLAP,  
        add_start_index=True,
    )

    all_splits = text_splitter.split_text(text)

    print(f"Split text into {len(all_splits)} chunks\n")
    return all_splits

