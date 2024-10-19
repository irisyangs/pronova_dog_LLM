# Pronova LLM Capstone Project

This repository will hold all information related to the Pronova LLM Capstone Project.

## Current Goals

- Collect information from reputable sources.
- Store the data in JSONL format and organize it in this repository.
- Create subfolders for each JSONL file, where each folder is named after the source.
- Combine all JSONL files into one large file to fine-tune the GPT-4o-mini model.
- Test the model with simple prompts as a proof of concept.

### system role ###
You are a specialized assistant that only provides advice on dog-related veterinary care. If a user asks about any other animal or topic outside of dog health, politely decline to answer and remind them that you only provide information about dogs.


## RAG description (Retrieval Augmented Generation) ##

To build a **RAG (Retrieval-Augmented Generation)** system using OpenAI’s GPT-4 (e.g., GPT-4.0-mini) and **Qdrant** (a popular vector database), you’ll create a pipeline where the model retrieves relevant information from a knowledge base stored in Qdrant and then generates a response based on that information. Here’s a step-by-step guide on how to set it up:

### 1. **Architecture Overview**
The main components of the RAG system are:
- **LLM (GPT-4)**: Handles the generation part (producing the response).
- **Qdrant Vector Database**: Stores vectorized representations of your reference texts (books, articles, veterinary data).
- **Retriever**: A system that performs the semantic search by querying Qdrant to find the most relevant chunks of text.
- **Pipeline**: Connects the retriever to the GPT model, allowing the model to access relevant context during generation.

### 2. **Set Up Qdrant for Document Storage and Retrieval**

**Qdrant** is a vector database optimized for fast and efficient semantic search. You’ll use Qdrant to store embeddings (vector representations) of your reference documents and retrieve relevant chunks based on the user’s query.

#### a. **Install Qdrant**
You can deploy Qdrant either locally or using cloud services. Here’s how to install it locally:

- Run Qdrant with Docker:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

Alternatively, you can use Qdrant Cloud for a managed solution: [Qdrant Cloud](https://cloud.qdrant.io/).

#### b. **Prepare Data and Generate Embeddings**
You’ll need to convert your documents into vector embeddings that Qdrant can store and search.

1. **Preprocessing the Data**: Break down your reference texts into smaller chunks (e.g., paragraphs or sections) that can be used for retrieval.
   ```python
   # Example of chunking large documents
   def chunk_text(text, chunk_size=1000):
       return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
   ```

2. **Embedding the Chunks**: Use OpenAI’s embedding models to convert each chunk into a vector.
   ```python
   import openai

   openai.api_key = 'your-api-key'

   def get_embedding(text):
       response = openai.Embedding.create(
           model="text-embedding-ada-002",
           input=text
       )
       return response['data'][0]['embedding']
   ```

3. **Upload Embeddings to Qdrant**:
   - Use Qdrant’s Python client to upload your document embeddings.

   ```python
   from qdrant_client import QdrantClient
   from qdrant_client.http.models import PointStruct

   # Connect to Qdrant
   client = QdrantClient(host="localhost", port=6333)

   # Create a collection to store embeddings
   client.create_collection(
       collection_name="veterinary_data",
       vector_size=1536,  # The dimensionality of embeddings
       distance="Cosine"  # Or "Euclidean"
   )

   # Upload embeddings
   points = [
       PointStruct(
           id=i,
           vector=get_embedding(chunk),
           payload={"text": chunk}
       )
       for i, chunk in enumerate(chunk_texts)
   ]
   client.upsert(
       collection_name="veterinary_data",
       points=points
   )
   ```

#### c. **Retrieve Relevant Chunks Based on User Query**
When the user asks a question, you’ll need to retrieve the top-N most relevant document chunks from Qdrant. To do this, first, convert the user’s query into an embedding and then query Qdrant for similar vectors.

```python
# Query Qdrant for relevant embeddings
def retrieve_relevant_chunks(query, top_k=5):
    query_embedding = get_embedding(query)

    search_result = client.search(
        collection_name="veterinary_data",
        query_vector=query_embedding,
        limit=top_k
    )

    return [result.payload["text"] for result in search_result]
```

### 3. **Integrate GPT-4 with the Retriever**
Once you retrieve the relevant chunks from Qdrant, you’ll pass them as context to OpenAI’s GPT-4 model.

#### a. **Combine Retrieved Chunks into Context**
Concatenate the most relevant chunks retrieved from Qdrant and pass them along with the user’s question to GPT-4 for generation.

```python
def generate_response(query):
    # Retrieve the relevant document chunks
    context = retrieve_relevant_chunks(query)

    # Concatenate context into a single string
    context_text = "\n".join(context)

    # Use GPT-4 to generate a response based on the context and user query
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Context: {context_text}\n\nQuestion: {query}\n\nAnswer:",
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()
```

#### b. **Fine-Tuning GPT-4 for Specific Domain**
To make GPT-4 more aligned with veterinary tasks, you could consider fine-tuning GPT-4 (or GPT-3.5) on a dataset of veterinary-specific Q&A. However, for most cases, GPT-4's base model can perform well when augmented with retrieval from Qdrant.

### 4. **Deployment and Optimization**

- **API Deployment**: If you're using Qdrant in the cloud, ensure your system can interact with both the GPT-4 API and the Qdrant instance. You may need to deploy this system as a backend API that your front-end (web or mobile app) can call.
- **Error Handling and Response Generation**: You’ll need to account for cases where no relevant context is found, or the context is insufficient, by having fallback mechanisms (e.g., having GPT-4 generate responses based solely on general knowledge when retrieval fails).
- **Performance**: Optimize for speed by caching frequently asked questions and embeddings, using batch retrieval for multiple queries, and monitoring latency between the retriever and GPT-4.

### 5. **Tools and Libraries**
- **OpenAI API**: For embeddings and completion generation.
- **Qdrant**: For the vector database.
- **Python Client Libraries**:
  - `openai`: For interacting with OpenAI’s GPT and embedding models.
  - `qdrant-client`: For working with Qdrant.

### Summary of Key Steps:
1. **Set up Qdrant** to store vectorized embeddings of your reference texts.
2. **Preprocess and embed your reference materials** using OpenAI embeddings.
3. **Use Qdrant to retrieve relevant chunks** based on user queries.
4. **Generate responses using GPT-4**, augmented with the retrieved information from Qdrant.
5. **Deploy and optimize** the system to handle multiple queries efficiently.

By using this RAG architecture with Qdrant and GPT-4, you can build a robust veterinary assistant that retrieves and integrates context from your large set of reference documents without overloading the model with unnecessary information upfront.