from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!", 200

@app.route('/call_hello', methods=['GET'])
def call_hello():
    try:
        # 替換成目標主機的 IP 和 Port
        target_host = "http://192.168.0.2:5000/hello"
        response = requests.get(target_host)
        return jsonify({
            "status": response.status_code,
            "message": response.text
        }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to call target host",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)