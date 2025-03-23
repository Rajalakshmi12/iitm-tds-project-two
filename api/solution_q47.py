import fitz  # PyMuPDF
from markdownify import markdownify
import subprocess
import os

#pip install fitz
#pip install frontend
#pip install markdownify 

def pdf_to_markdown(pdf_path, md_path):
    # Open PDF
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from all pages
    for page in doc:
        text += page.get_text("text") + "\n\n"
    print(text)

    # Convert to Markdown (basic formatting)
    markdown_text = markdownify(text)

    # Save to Markdown file
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_text)

    print(f"Markdown saved: {md_path}")

def format_markdown(md_path):
    # Run Prettier to format Markdown
    prettier_path = "C:\\Users\\poort\\AppData\\Roaming\\npm\\prettier.cmd"
    if os.path.exists(prettier_path):
        print('yes')
    subprocess.run([prettier_path, "--write", md_path])
    print(f"Markdown formatted: {md_path}")
    
    
# Convert PDF to Markdown
pdf_path = "q-pdf-to-markdown.pdf"  # Change this to your PDF file
md_path = "output.md"

if os.path.exists(pdf_path):
    print('yes')
pdf_to_markdown(pdf_path, md_path)
format_markdown(md_path)
