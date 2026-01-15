import sys
import asyncio
from process import extract_text_from_pdf, split_text
from pinecone_init import PineconeClient
from agent.agent import run_agent

async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py /path/to/syllabus.pdf optional_namespace")
        sys.exit(1)
    
    pdf_path = sys.argv[1]

    # Use a provided namespace from args, or generate from filename
    if len(sys.argv) > 2:
        namespace = sys.argv[2]
    else:
        # Auto-generate: "syllabus.pdf" -> "syllabus"
        namespace = pdf_path.split('/')[-1].replace('.pdf', '').replace(' ', '_')

    # Initialize Pinecone
    pinecone = PineconeClient()

    # Check if this syllabus already exists
    all_namespaces = pinecone.list_namespaces()

    if namespace in all_namespaces:
        print("Skipping upload, using cached version\n")

        vector_store = pinecone.get_vectorstore(namespace)
    else:
        print(f"📄 New syllabus detected: '{namespace}'")

        # Extract text from pdf
        print("Step 1: Extracting text...\n")
        text = extract_text_from_pdf(pdf_path)

        # Split into chunks
        print("Step 2: Split text into chunks...\n")
        chunks = split_text(text)
        
        # Step 3: Upload to Pinecone
        print("Step 3: Uploading to Pinecone...")
        vector_store = pinecone.upload_chunks(chunks, namespace)
        
    # Run agent
    print("Running agent...\n")
    await run_agent(vector_store)

if __name__ == "__main__":
    asyncio.run(main())