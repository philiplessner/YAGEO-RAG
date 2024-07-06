import sys
from html_ingest import HTMLIngest

filename = sys.argv[1]
with open(filename, "r") as f:
    files = [line.strip('\n') for line in f]

for file in files:
    test = HTMLIngest(file, 'div', 'cmp-container')
    test.html2elements()
    test.elements2chunks()
    test.chunks2docs()
    test.docs2db('./mydb')
    del test