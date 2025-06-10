import fitz  # PyMuPDF

# Path to your large PDF
pdf_path = "input.pdf"
output_png = "output.png"

# Open the PDF
doc = fitz.open(pdf_path)

# Get the first page
page = doc.load_page(0)  # 0-indexed

# Render page to a pixmap (PNG image)
pix = page.get_pixmap(dpi=300)  # Change DPI for higher/lower quality

# Save to PNG
pix.save(output_png)

print("Conversion completed successfully.")
