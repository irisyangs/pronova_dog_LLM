import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI

# Get the Qdrant API key from the environment variable
Qdrant_api_key = os.getenv('Qdrant_API_KEY')
if not Qdrant_api_key:
    raise ValueError("No Qdrant API key found in environment variables")


# Initialize Qdrant client
try:
    Qclient = QdrantClient(
        url="https://42695f66-c1b7-4300-8325-88f667b311ae.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key=Qdrant_api_key
    )
    print("Successfully connected to Qdrant")
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")
    raise

# Create collection
# try:
#     Qclient.create_collection(
#         collection_name="irf_rules",
#         vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
#     )
#     print("Collection 'irf_rules' created successfully")
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
    points = []
    for i, embedding in enumerate(embeddings):
        points.append(
            {
                "id": i,
                "vector": embeddings[i],
                "payload": {"text": chunks[i]}
            }
        )
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
# upsert_embeddings("irf_rules", embeddings, chunks)

def retrieve_relevant_chunks(query, top_k=5):
    query_embedding = get_embedding(query)
    
    search_result = Qclient.search(
        collection_name="irf_rules",
        query_vector=query_embedding,
        limit=top_k
    )

    return [result.payload["text"] for result in search_result]

def generate_response(query):
    context = retrieve_relevant_chunks(query)

    # Combine retrieved chunks into a single string
    context_text = "\n".join(context)

    # Generate a response using GPT-4
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing information about roundnet rules."},
            {"role": "user", "content": context_text},
            {"role": "user", "content": query}
        ]
    )
    return completion.choices[0].message

# Test the response generation
query = "What happens if you win a point while serving?"
relevant_chunks = retrieve_relevant_chunks(query)
# print(relevant_chunks)
response = generate_response(query)
print(response.content)



