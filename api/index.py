from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head><title>🤖 HH Bot OAuth @yanaoqa</title></head>
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
    
    print(f"DEBUG: code={code[:20] if code else 'None'}, state={state}")
    
    # ✅ АВТО ОТПРАВКА В TELEGRAM (НОВОЕ!)
    if code and state:
        bot_token = os.environ.get('BOT_TOKEN')
        if bot_token:
            bot_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            bot_data = {
                'chat_id': state,
                'text': "✅ **Авторизация успешна!**\n\n🎉 Добро пожаловать в бот для автоматического поиска работы!\n\n📋 Нажмите кнопку ниже:",
                'reply_markup': '{"inline_keyboard":[[{"text":"🚀 Открыть главное меню","callback_data":"main_menu_open"}]}',
                'parse_mode': 'Markdown'
            }
            response = requests.post(bot_url, json=bot_data)
            print(f"✅ Telegram: {response.status_code}")
    
    # ТВОЙ КОД ОСТАЁТСЯ!
    if code:
        try:
            with open('/tmp/hh_code.txt', 'w') as f:
                f.write(f"code={code}\nstate={state}")
            print("✅ Код сохранён")
        except Exception as e:
            print(f"⚠️ Сохранение: {e}")
        
        return f"""
<!DOCTYPE html>
<html>
<head><title>✅ Авторизация успешна!</title></head>
<body style="font-family: Arial; text-align: center; background: #d4edda;">
    <h1>✅ Авторизация успешна!</h1>
    <p>✅ Сообщение отправлено в Telegram!</p>
    <p><b>Code:</b> {code[:30]}...</p>
    <p><b>State:</b> {state}</p>
    <hr>
    <p><a href="https://t.me/yakorqa_resume_hh_bot">Открыть бота</a></p>
</body>
</html>
        """
    else:
        return """
<!DOCTYPE html>
<html>
<head><title>❌ Ошибка</title></head>
<body style="font-family: Arial; text-align: center; background: #f8d7da;">
<h1>❌ Ошибка авторизации</h1>
<p>Код не получен. Попробуй ещё раз.</p>
<p>Code: {code}<br>State: {state}</p>
</body>
</html>
        """.format(code=code or 'None', state=state)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
