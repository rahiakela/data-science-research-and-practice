import asyncio
import contextlib
import io
from pathlib import Path

from PIL import Image
from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from object_detection import ObjectDetection


# initiate object_detection instance
object_detection = ObjectDetection()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """It sure that the model is loaded during application startup and is ready to use."""
    object_detection.load_model()
    yield


app = FastAPI(lifespan=lifespan)


async def receive(websocket: WebSocket, queue: asyncio.Queue):
    """This method is for waiting for raw bytes from the WebSocket"""
    while True:
        raw_bytes = await websocket.receive_bytes()
        try:
            # drop images that we won’t be able to handle in time
            queue.put_nowait(raw_bytes)
        except asyncio.QueueFull:
            pass


async def detect(websocket: WebSocket, queue: asyncio.Queue):
    """This method is for performing the detection and sending the result"""
    while True:
        raw_bytes = await queue.get()
        # since we get raw image bytes directly
        image = Image.open(io.BytesIO(raw_bytes))
        detections = object_detection.predict(image)
        await websocket.send_json(detections.dict())


@app.websocket("/object-detection")
async def ws_object_detection(websocket: WebSocket):
    # open the web socket tunnel
    await websocket.accept()

    # create queue with 1 limit
    queue: asyncio.Queue = asyncio.Queue(maxsize=1)
    receive_task = asyncio.create_task(receive(websocket, queue))
    detect_task = asyncio.create_task(detect(websocket, queue))

    try:
        done, pending = await asyncio.wait({receive_task, detect_task}, return_when=asyncio.FIRST_COMPLETED,)
        for task in pending:
            task.cancel()
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass


@app.get("/")
async def index():
    return FileResponse("index.html")


static_files_app = StaticFiles(directory="assets")
app.mount("/assets", static_files_app)