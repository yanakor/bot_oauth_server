from flask import Flask, request, redirect
import requests
import os
import uuid

app = Flask(__name__)

CLIENT_ID = "PFBD02JSP78M0NQ65ABL5CM8O98Q6RADDCDBUQVP2KO07A9KS7Q2G3EM47U6MQIR"
CLIENT_SECRET = "Q16BLТОЙ_ПОЛНЫЙ_MI8RB"  # Твой Secret
BOT_TOKEN = "ТВОЙ_BOT_TOKEN"

@app.route('/')
def home():
    return """
<h1>🤖 HH Bot OAuth @yanaoqa</h1>
<p>✅ Server is running</p>
<p>This is an OAuth callback endpoint for HeadHunter authorization.</p>
    """

@app.route('/oauth/callback')
def hh_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    if code and state:
        # Обмен code → token
        url = "https://api.hh.ru/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': request.url_root + 'oauth/callback'
        }
        
        token_response = requests.post(url, data=data).json()
        
        if 'access_token' in token_response:
            token = token_response['access_token']
            
            # Отправляем токен в бот
            bot_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            bot_data = {
                'chat_id': state,
                'text': f"✅ **Авторизация успешна!**\n\n🎉 Добро пожаловать в бот для автоматического поиска работы на HeadHunter!\n\n📋 Нажмите кнопку ниже, чтобы открыть главное меню:",
                'reply_markup': '{"inline_keyboard":[[{"text":"Открыть главное меню","callback_data":"main_menu_open"}]]}',
                'parse_mode': 'Markdown'
            }
            
            requests.post(bot_url, json=bot_data)
            
            return f"""
<h1>✅ Авторизация успешна!</h1>
<p>Вы успешно авторизовались через HeadHunter.</p>
<p><a href="https://t.me/yakorqa_resume_hh_bot">Открыть бота</a></p>
            """
    
    return "<h1>❌ Ошибка авторизации</h1>"
