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

# Переменная для отслеживания состояния потока
stream_active = True
capture = Capture()  # Инициализация захвата

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

async def get_capture_stream(capture):
    while stream_active:  # Проверка состояния потока
        frame = await capture.get_frame()  # Await if it's a coroutine
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.get('/capture_stream')
async def capture_stream():
    return StreamingResponse(get_capture_stream(capture), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get('/start_stream')
async def start_stream():
    global stream_active
    stream_active = True
    return {"status": "Stream started"}

@app.get('/stop_stream')
async def stop_stream():
    global stream_active
    stream_active = False
    return {"status": "Stream stopped"}

@app.get('/last_frame')
async def last_frame():
    if capture.last_frame is not None:
        frame_jpeg = capture.get_last_frame()
        return StreamingResponse(io.BytesIO(frame_jpeg.tobytes()), media_type="image/jpeg")
    return {"error": "No frame available"}

if __name__ == '__main__':
    uvicorn.run("fast_api_server:app", port=80, access_log=False)