from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🤖 HH OAuth Server @yanaoqa ✅</h1>"

@app.route('/oauth/callback')
def callback():
    code = request.args.get('code')
    if code:
        with open('hh_code.txt', 'w') as f:
            f.write(code)
        return f"<h1>✅ Code: {code[:30]}... Сохранено!</h1>"
    return "<h1>❌ Нет кода</h1>"

if name == '__main__':
    app.run(port=3000)
