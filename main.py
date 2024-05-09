import os
import json
import nest_asyncio
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Response

# llm package
from llama_index.core import Settings

# custom package
from utils.functions import read_data_folder
from utils.vector_db import ChromaDBVector
from utils.embedding import OpenAIEmbed, GooglePalmEmbed
from utils.query_search import QuerySearch

nest_asyncio.apply()

# env variables
env_config = dotenv_values(".env")
if not env_config:
    raise Exception("Environment file not found")
os.environ["LLAMA_CLOUD_API_KEY"] = env_config["LLAMA_CLOUD_API_KEY"]
os.environ["OPENAI_API_KEY"] = env_config["OPENAI_API_KEY"]

# config file
config = json.load(open("config.json"))
if not config:
    raise Exception("Config file not found")

# config variables
storage_path = config.get("storage_path")
collection_name = config.get("collection_name")
result_type = config.get("result_type")
embed_type = config.get("embed_type")
data_path = config.get("data_path")

if not all([storage_path, collection_name, result_type, embed_type, data_path]):
    raise Exception("Config file is missing required fields")

if not os.path.exists(data_path):
    raise Exception("Data path does not exist")

documents_path = read_data_folder(data_path)

# embedding model type
if embed_type == "openai":

    embed_model = config.get("openai_embedding_model")
    generator_model = config.get("openai_generator_model")

    if not all([embed_model, generator_model]):
        raise Exception("Config file is missing required fields")

    openai_embedding = OpenAIEmbed(
        embedding_model=embed_model,
        generator_model=generator_model,
    )

    llm, embed_model = openai_embedding.init_embedding()
    Settings.llm = llm
    Settings.embed_model = embed_model

elif embed_type == "palm":

    embed_model = config.get("palm_embedding_model")

    if not embed_model:
        raise Exception("Config file is missing required fields")

    google_palm_embedding = GooglePalmEmbed(
        model_name=embed_model, api_key=env_config["GOOGLE_PALM_API_KEY"]
    )

    embed_model = google_palm_embedding.init_embedding()
    Settings.embed_model = embed_model

else:
    raise Exception("Invalid embedding type")

# ChromaDB
vectordb = ChromaDBVector()
storevector = vectordb.StoreVector(
    storage_path=storage_path,
    collection_name=collection_name,
    result_type=result_type,
    documents_path=documents_path,
)
loaddata = vectordb.LoadData(
    storage_path=storage_path,
    collection_name=collection_name,
    result_type=result_type,
    documents_path=documents_path,
)

# QuerySearch
searchdata = vectordb.QuerySearch(
    storage_path=storage_path, collection_name=collection_name
)

# load data initially
try:
    if not os.path.exists(storage_path) or not os.listdir(storage_path):
        loaddata.load_db()
    index = searchdata.load_index()
except Exception as e:
    raise Exception(str(e))

app = FastAPI()


@app.get("/")
def index_render():
    return Response(status_code=200, content="Welcome to the ChromaDB API")


@app.post("/db/reload")
def reload_db():
    """
    Delete the old database and reload the new one.
    """
    try:
        if os.path.exists(storage_path):
            os.remove(storage_path)
        loaddata.load_db()
        return Response(status_code=200, content="Database reloaded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search/query")
def search_query(query: str):
    """
    Search the query in the database and return the response.
    """

    try:
        searchquery = QuerySearch(query=query, index=index)
        response = searchquery.simple_search()

        response_json = json.loads(response.response)
        return Response(
            status_code=200,
            content=json.dumps(response_json),
            media_type="application/json",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
