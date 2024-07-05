import requests
from bs4 import BeautifulSoup
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class HTMLIngest():

    def __init__(self,
                 html_source:str, 
                 tag_type:str, 
                 tag_class:str) -> None:
        self.html_source = html_source
        self.tag_type = tag_type
        self.tag_class = tag_class
        self.elements = []
        self.chunks = []
        self.docs = []
    
    def html2elements(self):
        page = requests.get(self.html_source)
        soup = BeautifulSoup(page.text, 'html.parser')
        output = soup.find_all(self.tag_type, class_=self.tag_class)
        self.elements = partition_html(text=str(output[0]))

    def elements2chunks(self):
        '''
        Convert elements to chunks of text
        '''
        self.chunks = chunk_by_title(self.elements, 
                                combine_text_under_n_chars=100, 
                                max_characters=3000)

    def chunks2docs(self):
        metadata = {'source':self.html_source}
        for chunk in self.chunks:
            self.docs.append(Document(page_content=chunk.text,
                                        metadata=metadata))

    def docs2db(self, persist_directory:str):
        mydb = Chroma(embedding_function=OpenAIEmbeddings(),
                      persist_directory=persist_directory)
        ids = mydb.add_documents(self.docs)
        return ids