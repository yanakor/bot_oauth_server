from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🤖 HH Bot OAuth @yanaoqa ✅ Vercel</h1>"

@app.route('/oauth/callback')
def hh_callback():
    code = request.args.get('code')
    if code:
        print(f"✅ CODE: {code[:30]}...")
        return f"<h1>✅ Code: {code[:30]}... OK!</h1>"
    return "<h1>❌ Нет кода</h1>"
