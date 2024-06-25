import pandas as pd
import warnings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from utils.llmutils import get_openai
from typing import List
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator


prompt = ChatPromptTemplate.from_messages(
    [("system", """You are a helpful clinician and an expert in reading medical documentation. Please extract the useful information from the following section of medical documentation."""), ("user", "{input}")]
)

class MediaclDocs(BaseModel):
    """Extract information from the medical documentation"""

    date: str = Field(description="Important - extract the date of the described event like consulation, medical exam results, etc. Format %Y-%m-%d.")
    event_type: str = Field(description="What does this document describe? I.e Consultation, prescription, medical exam results, etc.")
    document_summary: str = Field(description="Thoroughly summarize the content. What is it about, findings and conclusions, what is the main issue, what is the treatment plan, recommendations, etc.")
    evaluation: str = Field(description="short and specific evaluation of the document like diagnosis, suspicion, or observation")
    page: str = Field(description="Extract page number. Could be in the following format 01/060")

def load_split_document(input_pdf:str, temp_folder:str):
    loader = TextLoader(f"{temp_folder}/{input_pdf}")
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=4000,
        chunk_overlap=1000,
        keep_separator=True,
        is_separator_regex=False,
    )
    sub_documents = text_splitter.split_documents(document)

    return sub_documents


def run():
    sub_documents = load_split_document(input_pdf='pdf_content.txt', temp_folder='temp')
    llm, _ = get_openai()

    parser = JsonOutputKeyToolsParser(key_name="MediaclDocs", first_tool_only=True)
    model = llm.bind_tools([MediaclDocs])
    chain = prompt | model | parser

    document_summary = []
    # TODO - remove dryrun!
    print('Prepaing medical documents summary...')
    try:
        for doc in sub_documents:
            response = chain.invoke({"input": doc.page_content})
            document_summary.append(response)
    except Exception as e:
        print(f"Error: {e}")

    if document_summary is None:
        raise ValueError("document_summary is None, cannot create DataFrame")

    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=UserWarning)

    df = pd.DataFrame(document_summary)
    df['date'] = pd.to_datetime(df['date'], exact=False, errors='coerce')
    df = df.sort_values(by='date', ascending=False)

    df.to_csv('data/medical_docs_summary.csv', index=False)

    print("Structured data extraction completed. Medical documents summary saved to data/medical_docs_summary.csv")

if __name__ == "__main__":
    run()
