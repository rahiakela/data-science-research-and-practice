import contextlib

from PIL import Image
from fastapi import FastAPI, File, UploadFile
from object_detection import ObjectDetection, Detections


# initiate object_detection instance
object_detection = ObjectDetection()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """It sure that the model is loaded during application startup and is ready to use."""
    object_detection.load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/object-detection", response_model=Detections)
async def post_object_detection(image: UploadFile = File(...)) -> Detections:
    image_object = Image.open(image.file)
    return object_detection.predict(image_object)
