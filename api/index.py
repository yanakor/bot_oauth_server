from flask import Flask, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.environ.get('HH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('HH_CLIENT_SECRET')  # Vercel Environment Variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # Vercel Environment Variable

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head><title>🤖 HH Bot OAuth @yanaoqa</title></head>
<body style="font-family: Arial; text-align: center;">
    <h1>🤖 HH Bot OAuth Server</h1>
    <p>✅ Server is running on Vercel</p>
    <p>OAuth2 callback для Telegram бота @yakorqa_resume_hh_bot</p>
    <hr>
    <p>🔐 Авторизация HeadHunter → Токен → Telegram</p>
</body>
</html>
    """
@app.route('/oauth/callback')
def hh_callback():
    code = request.args.get('code')
    state = request.args.get('state', 'none')  # Telegram chat_id!
    
    print(f"DEBUG: code={code[:20] if code else 'None'}, state={state}")
    
    if code and state and CLIENT_SECRET and BOT_TOKEN:
        print("🔄 Code → Token exchange...")
        
        # 1. Code → ACCESS TOKEN
        token_url = "https://api.hh.ru/token"
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': 'https://bot-oauth-server.vercel.app/oauth/callback'
        }
        
        token_response = requests.post(token_url, data=token_data).json()
        print(f"Token response: {token_response}")
        
        access_token = token_response.get('access_token')
        if access_token:
            print(f"✅ Token получен: {access_token[:20]}...")
            
            # 2. ТЕСТ API (проверка профиля)
            headers = {'Authorization': f"Bearer {access_token}"}
            me_response = requests.get("https://api.hh.ru/me", headers=headers).json()
            user_id = me_response.get('id', 'unknown')
            
            # 3. ОТПРАВЛЯЕМ ТОКЕН + МЕНЮ В TELEGRAM!
            bot_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            bot_data = {
                'chat_id': state,
                'text': (
                    "✅ **Авторизация успешна!**\n\n"
                    "🎉 Добро пожаловать в бот для автоматического поиска работы на HeadHunter!\n\n"
                    f"👤 HH ID: `{user_id}`\n"
                    "📱 Токен получен и активен (14 дней)\n\n"
                    "🚀 **Готов к откликам!** (200/день)\n\n"
                    "📋 Нажмите кнопку ниже:"
                ),
                'reply_markup': (
                    '{"inline_keyboard":['
                    '[{"text":"🚀 Главное меню","callback_data":"main_menu_open"}],'
                    '[{"text":"📖 Инструкция","url":"https://telegra.ph/Instrukciya-po-ispolzovaniu-bota-12-09"}]'
                    ']}'
                ),
                'parse_mode': 'Markdown'
            }
            
            tg_response = requests.post(bot_url, json=bot_data)
            print(f"✅ Telegram status: {tg_response.status_code} | Response: {tg_response.text[:100]}")
            
            return f"""
<!DOCTYPE html>
<html>
<head><title>✅ Авторизация завершена!</title></head>
<body style="font-family: Arial; text-align: center; background: #d4edda;">
    <h1>✅ Авторизация завершена!</h1>
    <p>Токен получен и отправлен в Telegram!</p>
    <p>HH ID: <b>{user_id}</b></p>
    <hr>
    <p><a href="https://t.me/yakorqa_resume_hh_bot">← Открыть бота @yakorqa_resume_hh_bot</a></p>
</body>
</html>
            """
        else:
            print(f"❌ Token error: {token_response}")
    
    return """
<!DOCTYPE html>
<html>
<head><title>❌ Ошибка авторизации</title></head>
<body style="font-family: Arial; text-align: center; background: #f8d7da;">
    <h1>❌ Ошибка авторизации</h1>
    <p>Не удалось получить токен. Попробуйте еще раз.</p>
    <p>Code: {} | State: {}</p>
    <hr>
    <p><a href="https://t.me/yakorqa_resume_hh_bot">← Вернуться в бот</a></p>
</body>
</html>
    """.format(code or 'None', state)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
