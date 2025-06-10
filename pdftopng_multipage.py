import fitz  # PyMuPDF
import os

# Path to your PDF file
pdf_path = "LOVNISH.pdf"
output_dir = "output_images"
dpi = 300  # You can change this for higher or lower image quality

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the PDF
doc = fitz.open(pdf_path)
page_count = len(doc)

# Iterate through all pages
for page_number in range(page_count):
    page = doc.load_page(page_number)  # 0-indexed
    pix = page.get_pixmap(dpi=dpi)

    # Generate a filename like "page_001.png"
    output_path = os.path.join(output_dir, f"page_{page_number + 1:03}.png")
    pix.save(output_path)
    print(f"Saved: {output_path}")

print("All pages converted successfully.")
