import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get the Qdrant API key from the environment variable
Qdrant_api_key = os.getenv('Qdrant_API_KEY')
if not Qdrant_api_key:
    raise ValueError("No Qdrant API key found in environment variables")
Qdrant_url = os.getenv('Qdrant_URL')
if not Qdrant_url:
    raise ValueError("No Qdrant URL found in environment variables")


# Initialize Qdrant client
try:
    Qclient = QdrantClient(
        url= Qdrant_url,
        api_key=Qdrant_api_key
    )
    print("Successfully connected to Qdrant")
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")
    raise

# Create collection
# try:
#     Qclient.create_collection(
#         collection_name="irf_rules_a",
#         vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
#     )
#     print("Collection 'irf_rules_a' created successfully")
# except Exception as e:
#     print(f"Failed to create collection: {e}")
#     raise

# Get the OpenAI API key from the environment variable
OpenAI_api_key = os.getenv('OPENAI_API_KEY')
if not OpenAI_api_key:
    raise ValueError("No OpenAI API key found in environment variables")

OpenAI.api_key = OpenAI_api_key

# Function to get the embedding of a text
def get_embedding(text):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

# Function to read a text file and chunk its content
def chunk_text_from_file(file_path, chunk_size=400):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to get embeddings for a list of text chunks
def get_embeddings_for_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
    return embeddings

# function to upsert embeddings into Qdrant
def upsert_embeddings(collection_name, embeddings, chunks):
    source_url = "https://example.com"
    points = []
    for i in range(len(embeddings)):
        print(f"upserting #{i}")
        points.append(
            {
                "id": i, 
                "vector": embeddings[i],     
                "payload": {
                    "text": chunks[i],   # Attach the chunk as payload
                    "source_url": source_url  # Add the source URL
                }
            }
        )
        # points.append(
        #     {
        #         "id": i,
        #         "vector": embeddings[i],
        #         "payload": {"text": chunks[i]}
        #     }
            
        # )
    try:
        Qclient.upsert(
            collection_name=collection_name,
            points=points
        )
        print("Embeddings upserted successfully")
    except Exception as e:
        print(f"Failed to upsert embeddings: {e}")
        raise

# create embeddings for the text file
# file_path = "irf_rules.txt"
# chunks = chunk_text_from_file(file_path)
# embeddings = get_embeddings_for_chunks(chunks)
# upsert_embeddings("irf_rules_a", embeddings, chunks)

def retrieve_relevant_chunks(query, top_k=5):
    query_embedding = get_embedding(query)
    
    search_result = Qclient.search(
        collection_name="irf_rules_a", # TODO fix this
        query_vector=query_embedding,
        limit=top_k
    )


    
    contexts = [result.payload["text"] for result in search_result]
    urls = [result.payload.get("source_url") for result in search_result]
    


    return contexts, urls
    # return [result.payload["text"] for result in search_result]


import numpy as np

def generate_response(query):
    context, urls = retrieve_relevant_chunks(query)
    
    # TODO assess this
    unique_urls = np.unique(urls)


    # Combine retrieved chunks into a single string
    context_text = "\n".join(context)

    # Generate a response using GPT-4
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing information about roundnet rules. Find the answer to the following question in the given context otherwise say that you dont know the answer."},
            {"role": "user", "content": "context" + context_text},
            {"role": "user", "content": query}
        ]
    )
    return completion.choices[0].message, unique_urls

# collections = Qclient.get_collections()
# print(collections)

# Test the response generation
query = "Can you wear cleats?" 
relevant_chunks = retrieve_relevant_chunks(query)
# print(relevant_chunks)
response, urls = generate_response(query)
print(response.content)


print(f"here are the urls: \n", [url for url in  urls])


