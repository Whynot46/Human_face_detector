import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from capture_proccesing import Capture
import asyncio
import io

app = FastAPI()
templates = Jinja2Templates(directory="templates")

capture = Capture()  # Инициализация захвата

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

async def get_capture_stream(capture):
    while capture.is_stream_active:  # Проверка состояния потока
        frame = await capture.get_frame()  # Await if it's a coroutine
        if frame is None:
            print("Ошибка: Кадр не получен, завершение потока.")
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.get('/capture_stream')
async def capture_stream():
    return StreamingResponse(get_capture_stream(capture), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get('/start_stream')
async def start_stream():
    print("Stream started")
    if not capture.is_stream_active:
        capture.is_stream_active = True
        capture.reconnect_to_stream()
    return {"status": "Stream started"}

@app.get('/stop_stream')
async def stop_stream():
    print("Stream stopped")
    capture.is_stream_active = False
    capture.video.release()
    return {"status": "Stream stopped"}

@app.get('/last_frame')
async def last_frame():
    last_frame_data = await capture.get_last_frame()
    if last_frame_data is None:
        return {"error": "Нет доступного последнего кадра."}
    return StreamingResponse(io.BytesIO(last_frame_data), media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)