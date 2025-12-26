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

if __name__ == "__main__":
    main()