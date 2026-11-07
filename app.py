import random
from flask import Flask

app = Flask(__name__)


# 1. トップページ (http://127.0.0)
@app.route("/")
def index():
    return "<h1>八幡平　産直掲示板</h1><p>こんにちはFlask！</p>"


# 2. 名前を受け取るページ (http://127.0.0hello/トモヤ など)
@app.route("/hello/<name>")
def hello(name):
    return f"<p>こんにちは{name}</p>"


# 3. おみくじページ (http://127.0.0omikuji)
@app.route("/omikuji")
def omikuji():
    results = ["大吉", "中吉", "小吉", "吉", "凶"]
    result = random.choice(results)
    return f"あなたの運勢は<strong>{result}</strong>です"


if __name__ == "__main__":
    # サーバーを起動
    app.run(debug=True)
