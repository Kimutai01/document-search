from flask import Flask, request, jsonify
from typing import Dict, Union
from flask_cors import CORS
# Third-Party Imports
from dotenv import load_dotenv
from llama_index.schema import NodeWithScore
import json
# Load environment variables from .env file
load_dotenv()

from orchestrator import generate_agent

class NodeWithScoreEncoder(json.JSONEncoder):
    """Custom JSON encoder for NodeWithScore objects."""
    
    def default(self, obj) -> Union[Dict, super]:
        if isinstance(obj, NodeWithScore):
            return obj.to_dict()
        return super().default(obj)



app = Flask(__name__)
CORS(app) 

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    chat_history = request.json.get('chat_history', [])
    agent = generate_agent(chat_history)
    response = agent.chat(user_input).__dict__
    chat_response = response['response']
    sources = json.loads(json.dumps(response['source_nodes'], cls=NodeWithScoreEncoder))

    return jsonify({
        "response": chat_response,
        "sources": sources
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7010, debug=False)
