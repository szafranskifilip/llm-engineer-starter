import os
from typing import Tuple, List
from enum import Enum
import openai

import dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

if not dotenv.load_dotenv():
    raise RuntimeError("Failed to load .env file")

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenaiConstants(Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4_TURBO = "gpt-4-turbo"

    def __str__(self) -> str:
        return self.value


def get_openai(model_name: str = str(OpenaiConstants.GPT_35_TURBO)) -> Tuple[ChatOpenAI, OpenAIEmbeddings]:

    llm = ChatOpenAI(model_name=model_name)
    embeddings = OpenAIEmbeddings()

    return llm, embeddings