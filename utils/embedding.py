from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.google import GooglePaLMEmbedding


class OpenAIEmbed:
    def __init__(self, embedding_model, generator_model):
        self.embedding_model = embedding_model
        self.generator_model = generator_model

    def init_embedding(self):
        llm = OpenAI(model=self.generator_model)
        embed_model = OpenAIEmbedding(model=self.embedding_model)
        return llm, embed_model


class GooglePalmEmbed:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key

    def init_embedding(self):
        embed_model = GooglePaLMEmbedding(
            model_name=self.model_name, api_key=self.api_key
        )
        return embed_model
