import fitz  # PyMuPDF
import sys
import json
import os

def extract_pdf_text(filepath):
    try:
        doc = fitz.open(filepath)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text("text")
        return text
    except Exception as e:
        return f"Error extracting {filepath}: {str(e)}"

if __name__ == "__main__":
    folder = "d:\\My Projects\\Capstone Project\\ProjectReport"
    pdfs = [
        "Bala Project Report Phase 1.pdf",
        "Journal Paper.pdf",
        "Project PPT Phase 1.pdf",
        "Team 011 Front 1.pdf",
        "Team 011 Project Report Phase 0.pdf"
    ]
    
    results = {}
    for pdf in pdfs:
        path = os.path.join(folder, pdf)
        results[pdf] = extract_pdf_text(path)
        
    with open(os.path.join(folder, "pdf_texts.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print("Extraction complete. Results saved to pdf_texts.json.")
