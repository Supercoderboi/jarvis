from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os
from datetime import datetime

app = Flask(__name__)

genai.configure(api_key="AIzaSyDGaF84zeUvIwwszRrAZ5Q-usOqQvZQ6zY")

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=(
        "You are JARVIS, Ethan Paul’s AI assistant. "
        "Speak with intelligence, professionalism, and a touch of witty British charm. "
        "Be clear, helpful, and slightly sarcastic when appropriate. "
        "Always act as a highly advanced and confident artificial intelligence system."
    )
)

LOG_FILE = "conversation_log.json"

def save_to_history(user_input, jarvis_reply):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "jarvis": jarvis_reply
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    user_input = data.get("text", "")

    try:
        response = model.generate_content(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Apologies, sir. I encountered an error: {e}"

    save_to_history(user_input, reply)

    return jsonify({"response": reply})

# ✅ NEW: /history route
@app.route('/history', methods=['GET'])
def get_history():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        return jsonify(history)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
