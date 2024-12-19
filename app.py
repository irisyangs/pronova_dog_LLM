from flask import Flask, request, jsonify
from flask_cors import CORS

collection_name = "LLM"

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/query', methods=['POST'])
def query_llm():
    data = request.json
    new_query = data.get('new_query')
    queries = data.get('queries')
    contexts = data.get('contexts')
    responses = data.get('responses')

    try:
        updated_queries, updated_contexts, updated_responses = generate_response(collection_name, new_query, queries, contexts, responses)
        return jsonify({
            'queries': updated_queries,
            'contexts': updated_contexts,
            'responses': updated_responses
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
