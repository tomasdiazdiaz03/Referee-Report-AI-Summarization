import pdfplumber

def extract_all_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

if __name__ == "__main__":
    print(extract_all_text_from_pdf("data/raw/sample.pdf"))