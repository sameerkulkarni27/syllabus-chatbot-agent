import sys
import asyncio
from process import extract_text_from_pdf, split_text
from embedding import Embedding
from agent.agent import run_agent


async def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py /path/to/syllabus.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Extract text from pdf
    text = extract_text_from_pdf(pdf_path)
    
    # Split into chunks
    chunks = split_text(text)
    
    # Create vector store
    embedding_manager = Embedding()
    vector_store = embedding_manager.create_vector_store(chunks)
    
    # Run agent
    await run_agent(vector_store)

if __name__ == "__main__":
    asyncio.run(main())