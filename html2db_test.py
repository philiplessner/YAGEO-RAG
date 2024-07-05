from html_ingest import HTMLIngest

with open("./data/KEMET_FAQs.txt", "r") as f:
    files = [line.strip('\n') for line in f]

for file in files:
    test = HTMLIngest(file, 'div', 'datasheet-content')
    test.html2elements()
    test.elements2chunks()
    test.chunks2docs()
    test.docs2db('./mydb')
    del test