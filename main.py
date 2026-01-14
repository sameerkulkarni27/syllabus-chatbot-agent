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
    print("Step 1: Extracting text...\n")
    text = extract_text_from_pdf(pdf_path)

    # Split into chunks
    print("Step 2: Split text...\n")
    chunks = split_text(text)
    
    # Create vector store
    print("Step 3: Create vector store...\n")
    embedding_manager = Embedding()
    vector_store = embedding_manager.create_vector_store(chunks)
    
    # Run agent
    print("Step 4: Run agent...\n")
    await run_agent(vector_store)

if __name__ == "__main__":
    asyncio.run(main())