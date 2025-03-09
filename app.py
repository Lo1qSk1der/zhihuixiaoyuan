from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"  # 请替换为实际API地址

@app.route("/")
def zhuYe():
    return "hello world!"
@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",  # 替换实际模型名称
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return jsonify({
            "response": result['choices'][0]['message']['content']
        })
    except Exception as e:
        return jsonify({"response": f"API请求失败: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)