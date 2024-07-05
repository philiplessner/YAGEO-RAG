import sys
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from markdownify import markdownify as md
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_retriver (persist_directory:str):
    vectorstore = Chroma(persist_directory=persist_directory,
                         embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="similarity",
                                         search_kwargs={"k": 3})
    return retriever


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


if __name__ == '__main__':
    query:str = sys.argv[1]
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    prompt = hub.pull("rlm/rag-prompt")

    example_messages = prompt.invoke(
        {"context": "filler context", "question": "filler question"}
    ).to_messages()

    retriever = get_retriver('./mydb')
    retrieved_documents = retriever.invoke(query)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print('\n', '****Answer****')
    for chunk in rag_chain.stream(query):
        print(chunk, end="", flush=True)
    print('\n\n', '****Based on the Following Context****')
    print_retrieved_documents(retrieved_documents)