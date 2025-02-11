#!/usr/bin/env python
# coding: utf-8

# # Pronova LLM Run Model #
# ## Use this notebook to do the following ##
# - Run the current model on a query
# - start a flask api server that accepts a query and will return a response

# In[ ]:


# Load require libraries
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Markdown, display

# Load environment variables from .env file
load_dotenv()


# ### Setup Qdrant connection ###

# In[ ]:


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


# ### Setup OpenAI connection ###

# In[ ]:


# Get the OpenAI API key from the environment variable
OpenAI_api_key = os.getenv('OPENAI_API_KEY')
if not OpenAI_api_key:
    raise ValueError("No OpenAI API key found in environment variables")

OpenAI.api_key = OpenAI_api_key


# ### Get an OpenAI embedding from a text segment (Function) ###

# In[ ]:


# Function to get the embedding of a text
def get_embedding(text):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding


# ### Retrieve similar chunks from query (Function) ###

# In[ ]:


def retrieve_relevant_chunks(collection_name, query, top_k=10):
    query_embedding = get_embedding(query)
    
    search_result = Qclient.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )

    contexts = [result.payload["text"] for result in search_result]
    files = [result.payload.get("source_file") for result in search_result]
    
    return contexts, files


# ### Rank response source importance (Function) ###

# In[ ]:


from collections import Counter

def file_ratios(files):
    total_files = len(files)
    counts = Counter(files)
    return {file: count*100 / total_files for file, count in counts.items()}


# file_ratios(["a", "a", "b", "c"])
# {'a': 0.5, 'b': 0.25, 'c': 0.25}


# ### Markdown Print Function ###

# In[ ]:


def print_markdown(md_text):
    display(Markdown(md_text))


# ### Generate Response from Query (Function) ###

# In[ ]:


import numpy as np

def generate_response(collection_name, query, all_query, all_context, all_responses):
    print("Generating response for query:", query)
    # generate context for new query
    context, files = retrieve_relevant_chunks(collection_name, query)
    
    files_used = np.unique(files)
    # files_used = file_ratios(files_used)

    system_role = "You are a specialized assistant that only provides advice on dog-related veterinary care. If a user asks about any other animal or topic outside of dog health, politely decline to answer and remind them that you only provide information about dogs. You will always start by asking the user their dog's name, age, and breed if they didn't already provide it."
    # Combine retrieved chunks into a single string
    context_text = "\n".join(context)

    # append query and context to the running lists
    all_query.append(query)
    all_context.append(context_text)

    # create the messages object using all the queries and contexts
    messages = [{"role": "system", "content": system_role}]

    for i in range(len(all_query)):
        messages.append({"role": "system", "content": "Use this context to answer my following question: " + all_context[i]})
        messages.append({"role": "user", "content": all_query[i]})
        if i < len(all_responses):
            messages.append({"role": "system", "content": all_responses[i]})
    
    # print(messages)


    # Generate a response using GPT-4
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )
    all_responses.append(completion.choices[0].message.content)
    return all_query, all_context, all_responses, files_used


# ### Playground (use this to test querys in the notebook)

# In[ ]:


# collection_name = "LLM_V1"
# query = "After we walk, my dog is always itchy"
# response, file_rank = generate_response(collection_name, query)
# print_markdown(response.content)


# print("files used: \n")
# for file in file_rank:
#     print(f"{file}, {file_rank[file]} %")


# ### Lightweight Flask Server (for Frontend API testing) ###

# In[ ]:


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, send_from_directory, render_template



# app = Flask(__name__)

## idk bruh

# app = Flask(__name__)

app = Flask(__name__, static_folder="LLM_Proof_Of_Concept/dist", static_url_path="")

CORS(app)  # This will enable CORS for all routes

# @app.route("/") 
# def index():
#     return render_template("chat.html", text="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# def home(): 
#     return "Hello, World!"

@app.route('/query', methods=['POST'])
def query_llm():

    data = request.json
    print(data)

    new_query = data.get('new_query')
    queries = data.get('queries')
    contexts = data.get('contexts')
    responses = data.get('responses')
    collection_name = "pronova-start"
    # maybe have a check if the collection name is in Qclient.collections
    
    # if not new_query or not queries or not contexts or not responses:
    #     return jsonify({'error': 'New query, queries, contexts, and responses must be provided'}), 400

    try:
        updated_queries, updated_contexts, updated_responses, files_used = generate_response(collection_name, new_query, queries, contexts, responses)
        response_data = {
            'queries': updated_queries,
            'contexts': updated_contexts,
            'responses': updated_responses,
            'files': files_used.tolist() if isinstance(files_used, np.ndarray) else files_used
        }
        print("Response data:", response_data)
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# # if __name__ == '__main__':
# print("Starting da server")
# port = int(os.environ.get('PORT', 5000))
# # app.run(host='0.0.0.0')

# app.run(host='0.0.0.0', port=port)



if __name__ == '__main__':
    print("Starting the server")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)