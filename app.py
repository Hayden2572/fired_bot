from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import uvicorn

app = FastAPI()

# Подключение статических файлов (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Главная страница Web App
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.query_params.get("user", "Гость")  # Получаем параметры из URL
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Web App</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Привет, {user}!</h1>
        <button onclick="sendData()">Отправить данные боту</button>

        <script>
            function sendData() {{
                Telegram.WebApp.sendData(JSON.stringify({{ message: "Привет от Web App!" }}));
            }}
        </script>
    </body>
    </html>
    """

# Обработка данных, если потребуется
@app.post("/process_data")
async def process_data(request: Request):
    data = await request.json()
    print(f"Получены данные: {data}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")