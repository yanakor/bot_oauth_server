from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head><title>HH Bot OAuth @yanaoqa</title></head>
<body style="font-family: Arial; text-align: center;">
    <h1>🤖 HH Bot OAuth Server</h1>
    <p>✅ Server is running</p>
    <p>This is an OAuth callback endpoint for HeadHunter authorization.</p>
    <hr>
    <p>Бот: @yakorqa_resume_hh_bot</p>
</body>
</html>
    """

@app.route('/oauth/callback')
def hh_callback():
    code = request.args.get('code')
    state = request.args.get('state', 'none')
    
    if code:
        with open('/tmp/hh_code.txt', 'w') as f:
            f.write(f"code={code}\nstate={state}")
        
        return f"""
<!DOCTYPE html>
<html>
<head><title>✅ Авторизация успешна!</title></head>
<body style="font-family: Arial; text-align: center;">
    <h1>✅ Код авторизации получен!</h1>
    <p><b>Code:</b> {code[:30]}...</p>
    <p><b>State:</b> {state}</p>
    <hr>
    <p>Вернись в Telegram бота @yakorqa_resume_hh_bot</p>
</body>
</html>
        """
    return "<h1>❌ Ошибка авторизации</h1>"

if __name__ == '__main__': 
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
