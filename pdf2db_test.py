import sys
from pdf_ingest import PdfIngest


filename = sys.argv[1]
with open(filename, "r") as f:
    files = [line.strip('\n') for line in f]

for file in files:
    pdf2db = PdfIngest(file)
    pdf2db.pdf2elements()
#    pdf2db.clean_elements()
    pdf2db.elements2chunks()
    pdf2db.chunks2docs()
    pdf2db.docs2db("./mydb")
    del pdf2db

