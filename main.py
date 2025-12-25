import sys
from process import extract_text_from_pdf, split_text


def main():
    # Check if PDF path provided
    if len(sys.argv) != 2:
        print("Usage: python main.py /path/to/syllabus.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    
    # # Test 3: Preview results
    # print("="*60)
    # print("📊 RESULTS")
    # print("="*60)
    # print(f"Total text length: {len(text)} characters")
    # print(f"Number of chunks: {len(chunks)}")
    # print(f"\n--- First Chunk Preview ---")
    # print(chunks[0][:300] + "..." if len(chunks[0]) > 300 else chunks[0])
    # print(f"\n--- Last Chunk Preview ---")
    # print(chunks[-1][:300] + "..." if len(chunks[-1]) > 300 else chunks[-1])
    # print("\n✅ Processing test complete!")

if __name__ == "__main__":
    main()