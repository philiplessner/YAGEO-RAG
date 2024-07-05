import sys
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from markdownify import markdownify as md


def search_documents(query:str, persist_directory:str):
    vectorstore = Chroma(persist_directory=persist_directory,
                         embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="similarity",
                                         search_kwargs={"k": 3})
    return retriever.invoke(query)


def print_retrieved_documents(retrieved_documents):
    print(f"Number of Retrieved Documents: {len(retrieved_documents)}\n")
    for i, retrieved_document in enumerate(retrieved_documents):
        print(f"Document Number {i}")
        print(retrieved_document.page_content)
        print("\n")
        table_html = retrieved_document.metadata.get('text_as_html', '')
        print(md(table_html))
        print("\n")
        print('Source Document: ', 
              retrieved_document.metadata.get('source', ''))
        print('\n')


if __name__ == "__main__":
    query:str = sys.argv[1]
    retrieved_documents = search_documents(query,
                                           "mydb")
    print_retrieved_documents(retrieved_documents)
