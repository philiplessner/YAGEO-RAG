## RAG for YAGEO ##

This repository contains data and code for building a RAG app for YAGEO data

|Program|Purpose|
|-------|-------|
|pdf_ingest.py|Contains PdfIngest class to<br>Get elements<br>Clean elements<br>Combine elements into text chunks<br>Transform chunks to LangChain docs<br>Vectorize docs and store in Chroma database|
|pdf2db_test.py|Uses PdfIngest class to take a list of pdf files and embeded the vectorized chunks in a vector database|
|html_ingest.py|Contains HTMLIngest class to<br>Get HTML using requests<br>Filter HTML to the relevant part using BeautifulSoup<br>Get elements<br>Combine elements into text chunks<br>Transform chunks into LangChain docs<br>Vectorize docs and store in Chroma database|
|html2db_test.py|Use HTMLIngest class to take a list of html web pages and embeded the vectorized chunks in a vector database|
|search.py|Search for documents in the vector database from a query string|
|ragchat.py|Search for documents matching the query and pass them to the LLM to use as context in answering the query|

