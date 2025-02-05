from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

OLLAMA_HOST = 'http://localhost:11434'

@app.route("/optimize", methods=["POST"])
def optimize_prompt():
    data = request.json
    prompt = data.get("prompt", "").strip()
    tone = data.get("tone", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400
    if not tone:
        return jsonify({"error": "Tone is required."}), 400

    # Construct the optimization instruction
    system_message = f"""Optimize the following prompt in a {tone} tone. 
    Make it more effective while maintaining the original intent. 
    Return only the optimized version without additional commentary."""

    try:
        response = requests.post(
            f'{OLLAMA_HOST}/api/chat',
            json={
                'model': 'deepseek',
                'messages': [
                    {'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': prompt}
                ],
                'stream': False
            }
        )

        if response.status_code == 200:
            optimized = response.json()['message']['content']
            return jsonify({"optimized_prompt": optimized})
            
        return jsonify({"error": f"Ollama API error: {response.text}"}), 500

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not connect to Ollama. Make sure it's running."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)