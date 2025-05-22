import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger

def merge_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    merger = PdfMerger()
    for f in files:
        merger.append(f)
    merger.write("merged.pdf")
    merger.close()
    print("PDFs Merged!")

tk.Tk().withdraw()
merge_pdfs()
