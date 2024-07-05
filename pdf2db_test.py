from pdf_ingest import PdfIngest

files = ["data/pdf/KEM_T2018_T528.pdf",
         "data/pdf/KEM_T2030_T522.pdf",
         "data/pdf/KEM_T2076_T52X-530.pdf",
         "data/pdf/KEM_T2079_SSD.pdf",
         "data/pdf/KEM_T2085_F-PS.pdf"]

for file in files:
    pdf2db = PdfIngest(file)
    pdf2db.pdf2elements()
    pdf2db.clean_elements()
    pdf2db.elements2chunks()
    pdf2db.chunks2docs()
    pdf2db.docs2db("./mydb")
    del pdf2db

