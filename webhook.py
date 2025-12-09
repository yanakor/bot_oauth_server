from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import sqlite3
import logging
from urllib.parse import urlparse, parse_qs
import time

app = FastAPI()
logger = logging.getLogger(__name__)

# ✅ БАЗА ДАННЫХ для временного хранения кодов
def init_db():
    conn = sqlite3.connect('auth_codes.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS auth_codes (
            code TEXT PRIMARY KEY,
            user_id TEXT,
            created_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def root():
    return {"status": "HH Auth Webhook готов"}

@app.get("/auth")
async def auth_callback(code: str = Query(...), state: str = Query(None)):
    """🎯 Автоматически сохраняем код по user_id из state"""
    logger.info(f"🔗 Получен code={code[:20]}..., state={state}")
    
    # ✅ Парсим user_id из state (5332584958_1765304784 → user_id=5332584958)
    try:
        user_id = state.split("_")[0]
    except:
        user_id = "unknown"
    
    # ✅ Сохраняем код в БД
    conn = sqlite3.connect('auth_codes.db')
    conn.execute(
        "INSERT OR REPLACE INTO auth_codes (code, user_id, created_at) VALUES (?, ?, ?)",
        (code, user_id, int(time.time()))
    )
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Код сохранен для user_id={user_id}")
    
    # ✅ Редирект в Telegram бот
    return HTMLResponse(f"""
    <html>
    <head><meta charset="UTF-8">
    <title>✅ Авторизация успешна!</title>
    <meta http-equiv="refresh" content="3;url=https://t.me/yanaoqa_hh_bot">
    </head>
    <body style="font-family:Arial;text-align:center;padding:50px;background:#4CAF50;color:white;">
        <h1>🎉 Авторизация прошла успешно!</h1>
        <p>Код авторизации сохранен</p>
        <p>User ID: <b>{user_id}</b></p>
        <p>Через 3 сек вернетесь в <b>@yanaoqa_hh_bot</b></p>
        <a href="https://t.me/yanaoqa_hh_bot" style="color:#fff;font-size:20px;">← В бот</a>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
