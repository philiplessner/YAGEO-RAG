from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain


class PdfIngest():
    '''
    Get pdf, split it into the elements present in the pdf
    Perform cleanup on the elements
    Spilt or combine the elements into chunks
    Write the chunks into LangChain Documents
    Vectorize chunks to Chroma
    '''


    def __init__(self, pdf_filepath:str):
        self.pdf_filepath = pdf_filepath
        self.elements = []
        self.chunks = []
        self.docs = []
    
    def pdf2elements (self):
        '''
        Partion the pdf into its elements
        E.g., Titles, Headings, Text, Tables, etc.
        '''
        self.elements = partition_pdf(self.pdf_filepath,
                            infer_table_structure=True,
                            extract_images_in_pdf=False,
                            strategy="hi_res")

    def clean_elements(self):
        # Clean up
        strings2replace = ['\u00A9 KEMET Electronics Corporation \u2022 One East Broward Boulevard Fort Lauderdale, FL 33301 USA \u2022 954-766-2800 \u2022 www.kemet.com', 
                        'KEMET a YAGEO company', 'KEMET a company', 'YAGEO',
                        'KEMET is a registered trademark of KEMET Electronics Corporation.']
        for el in self.elements:
            for string2replace in strings2replace:
                if (string2replace in el.text):
                    x = el.text.replace(string2replace, "")
                    el.text = x

    def elements2chunks(self):
        '''
        Convert elements to chunks of text
        '''
        self.chunks = chunk_by_title(self.elements, 
                                combine_text_under_n_chars=100, 
                                max_characters=3000)

    def print_chunks(self):
        for chunk in self.chunks:
            if (chunk.category == 'Table'):
                print(chunk.metadata.text_as_html)
            else:
                print(chunk.text)
            print("\n\n" + "-"*80)


    def chunks2docs(self):
        '''Convert Chunks for LangChain Documents'''
        for chunk in self.chunks:
            if(chunk.category == 'Table'):
                text_summary = PdfIngest.table_summary(chunk.metadata.text_as_html)
                table_metadata = {'source':chunk.metadata.filename,
                                  'page_number':chunk.metadata.page_number,
                                  'text_as_html': chunk.metadata.text_as_html} 
                self.docs.append(Document(page_content=text_summary,
                                          metadata=table_metadata))
            else:
                metadata = {'source':chunk.metadata.filename,
                            'page_number':chunk.metadata.page_number}
                self.docs.append(Document(page_content=chunk.text,
                                          metadata=metadata))

    def docs2db(self, persist_directory:str):
        mydb = Chroma(embedding_function=OpenAIEmbeddings(),
                      persist_directory=persist_directory)
        ids = mydb.add_documents(self.docs)
        return ids
         #Chroma.from_documents(documents=self.docs,
         #                     embedding=OpenAIEmbeddings(),

    @staticmethod
    def table_summary(table_html:str) -> str:
        llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-1106')
        chain = load_summarize_chain(llm, chain_type='stuff')
        out_dict = chain.invoke([Document(page_content=table_html)])
        return out_dict['output_text']