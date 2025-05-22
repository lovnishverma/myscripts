import os
from PyPDF2 import PdfMerger

merger = PdfMerger()
pdf_folder = "pdfs"

for filename in sorted(os.listdir(pdf_folder)):
    if filename.endswith(".pdf"):
        merger.append(os.path.join(pdf_folder, filename))

merger.write("merged_output.pdf")
merger.close()
