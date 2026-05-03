from flask import Flask, request, redirect, jsonify
import redis
import string
import random

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def home():
    return "URL Shortener Running 🚀"

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    long_url = data.get('url')

    short_code = generate_short_code()
    r.set(short_code, long_url)

    return jsonify({
        "short_url": f"http://localhost:30007/{short_code}"
    })

@app.route('/<code>')
def redirect_url(code):
    long_url = r.get(code)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)