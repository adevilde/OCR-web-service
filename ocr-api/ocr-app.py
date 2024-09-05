from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import base64
import io
import uuid
import asyncio
from PIL import Image
import pytesseract

# Create a new FastAPI instance
app = FastAPI()

# Simulating a database with a dictionary
# it stores and tracks the status or results of asynchronous tasks
task_store = {}

# Pydantic model to validate and structure incoming image data as a Base64 string
class ImageData(BaseModel):
    image_data: str

# Pydantic model to validate and structure incoming task ID data
class TaskID(BaseModel):
    task_id: str


def decode_image(image_data: str):
    try:
        """Decode an image from base64 encoding."""
        image_bytes = base64.b64decode(image_data) # Decode the base64 string
        image = Image.open(io.BytesIO(image_bytes)) # Open the image from bytes
        return image
    except Exception as e:
        print(f"Error decoding image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    """Home endpoint to guide users."""
    return "Welcome to the OCR app! Use /image-sync for synchronous OCR or /image for asynchronous OCR."


@app.post("/image-sync")
def image_sync(image_data: ImageData):
    """Synchronously handle OCR processing."""
    image_data_str = image_data.image_data # Decode the image data from base64 string
    image = decode_image(image_data_str)
    
    # Check if the image needs to be rotated
    if image.width < image.height:
        image = image.rotate(-90, expand=True)
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    return {"text": text}


async def perform_ocr(image_data: str):
    """Asynchronously perform OCR on the given image."""
    image = decode_image(image_data) # Decode the image data from base64 string
    loop = asyncio.get_running_loop() # G   et the running event loop
    
    # Check if the image needs to be rotated
    if image.width < image.height:
        image = image.rotate(-90, expand=True)
    
    # Run pytesseract image to string conversion in an executor to not block async loop
    text = await loop.run_in_executor(None, pytesseract.image_to_string, image)
    return text


async def update_task_store(task_id: str, image_data: str):
    """Update the task store with the result of the OCR operation."""
    result = await perform_ocr(image_data) # Perform OCR on the image data asynchronously
    task_store[task_id] = result # Store the result with associated task ID


@app.post("/image")
async def image_async(image_data: ImageData):
    """Asynchronously handle OCR processing and return a task ID."""
    task_id = str(uuid.uuid4()) # Generate a unique task ID
    task_store[task_id] = None  # Initialize the task status with None
    # Start a new task to update the task store with the OCR result
    asyncio.create_task(update_task_store(task_id, image_data.image_data))
    return {"task_id": task_id}


@app.get("/image")
async def get_image_result(task_data: TaskID = Body(...)):
    """Retrieve OCR result using a task ID."""
    task_id = task_data.task_id
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task ID not found")
    
    result = task_store[task_id]
    if result is None:
        return JSONResponse(content={"task_id": None}, status_code=202)
    else:
        return {"task_id": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
