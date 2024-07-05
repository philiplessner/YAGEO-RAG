from typing import Sequence
import bs4
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.merge import MergedDataLoader

def web2docs(web_pages: Sequence[str], div_class: Sequence[str]) -> list:
    '''Get html documents from web
    Parameters
    web_page: list or tuple of strings with web address of pages
    div_class: div classes on page to keep
    Return
    docs object with content and metadata
    '''
    bs4_strainer = bs4.SoupStrainer(class_=div_class)
    loader = WebBaseLoader(
                           web_paths=web_pages,
                           bs_kwargs={"parse_only": bs4_strainer},)
    return loader


def get_websites(filepath:str) -> Sequence[str]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip('\n') for line in f]


def print_doc_info(docs: list) -> None:
    print("Doc#      Length      Source")
    for i, doc in enumerate(docs):
        print(f"{i}         {len(doc.page_content)}       {doc.metadata}")


def split_text(docs: list):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=200,
                                                   add_start_index=True)
    return text_splitter.split_documents(docs)


def vectorize_splits(splits, persist_directory):
    Chroma.from_documents(documents=splits,
                          embedding=OpenAIEmbeddings(),
                          persist_directory=persist_directory)


if __name__ == "__main__":
    web_pages = ("https://www.kemet.com/en/us/capacitors/ceramic/ceramics-faq.html",
                 "https://www.kemet.com/en/us/capacitors/polymer/tantalum-polymer-faqs.html")
    docs = web2docs(web_pages, ("datasheet-content"))
    docs2 = web2docs(get_websites ("./data/KEMET_Technical_Blogs.txt"), "cmp-container")
    loader_all = MergedDataLoader(loaders=[docs, docs2])
    all_docs = loader_all.load()
    print_doc_info(all_docs)
    all_splits = split_text(all_docs)
    print(f"The length of all_splits is {len(all_splits)}")
    vectorize_splits(all_splits, 'vector_db')
