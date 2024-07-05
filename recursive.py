
from typing import Sequence
import re
import bs4
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.merge import MergedDataLoader


def filter(html:str) -> str:
    parse_divs = bs4.SoupStrainer("div", attrs={"class": "cmp-container"})
    soup = bs4.BeautifulSoup(html, 'html.parser', parse_only=parse_divs)
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


def web_recursive_load(root_site:str, filter_func):
    loader = RecursiveUrlLoader(root_site, extractor=filter_func)
    return loader


def print_doc_info(docs: list) -> None:
    print("Doc#      Length      Source")
    for i, doc in enumerate(docs):
        print(f"{i}         {len(doc.page_content)}       {doc.metadata}")


def split_text(docs: list):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=200,
                                                   add_start_index=True)
    return text_splitter.split_documents(docs)


if __name__ == "__main__":
    # docs = web_recursive_load("https://www.kemet.com/en/us/technical-resources.html", filter)
    loader =RecursiveUrlLoader("https://www.kemet.com/en/us/technical-resources/", max_depth=2)
    docs = loader.load()
    print_doc_info(docs)
    print(docs[0].page_content[:1000])