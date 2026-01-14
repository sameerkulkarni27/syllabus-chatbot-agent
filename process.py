from PyPDF2 import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(pdf_path): 
    """Extract text from PDF file"""

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()  + "\n"

    return text

def split_text(text): 
    """Split the text into chunks"""
    text_splitter = SemanticChunker(
        OpenAIEmbeddings(),
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95  
    )

    all_splits = text_splitter.split_text(text)

    return all_splits