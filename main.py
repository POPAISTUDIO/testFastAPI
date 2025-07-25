from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Union
import os
import base64
import mimetypes
from io import BytesIO
from PIL import Image
import json
from dotenv import load_dotenv
from runwayml import RunwayML, TaskFailedError
import argparse

# Load environment variables
load_dotenv()

app = FastAPI(title="Image Generation API", description="Generate images using Runway API")

class ReferenceImage(BaseModel):
    base64_image: str  # base64 encoded image (not data URI)
    tag: Optional[str] = None
    filename: Optional[str] = None

class ReferenceImageURL(BaseModel):
    url: str
    tag: Optional[str] = None

class GenerateImageRequest(BaseModel):
    prompt_text: str
    model: str = "gen4_image"
    ratio: str = "1024:1024"
    reference_images: Optional[List[ReferenceImage]] = None

class GenerateImageURLRequest(BaseModel):
    prompt_text: str
    model: str = "gen4_image"
    ratio: str = "1024:1024"
    reference_images: Optional[List[ReferenceImageURL]] = None

class GenerateImageResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Image Generation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def get_data_uri(image_bytes: bytes, filename: Optional[str] = None) -> str:
    if filename:
        content_type = mimetypes.guess_type(filename)[0] or "image/png"
    else:
        content_type = "image/png"
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{content_type};base64,{base64_image}"

@app.post("/generateimage", response_model=GenerateImageResponse)
async def generate_image(
    prompt_text: str = Form(...),
    model: str = Form("gen4_image"),
    ratio: str = Form("1024:1024"),
    reference_image_1: Optional[UploadFile] = File(None),
    reference_image_1_tag: Optional[str] = Form(None),
    reference_image_2: Optional[UploadFile] = File(None),
    reference_image_2_tag: Optional[str] = Form(None),
    reference_image_3: Optional[UploadFile] = File(None),
    reference_image_3_tag: Optional[str] = Form(None)
):
    try:
        # Initialize RunwayML client with API key
        runway_api_key = os.getenv("RUNWAYML_API_SECRET")
        if not runway_api_key:
            raise HTTPException(status_code=500, detail="Runway API key not configured")
        client = RunwayML(api_key=runway_api_key)
        
        # Prepare reference images as data URIs with tags
        reference_images = []
        for ref_img, tag in [
            (reference_image_1, reference_image_1_tag),
            (reference_image_2, reference_image_2_tag),
            (reference_image_3, reference_image_3_tag)
        ]:
            if ref_img:
                image_bytes = await ref_img.read()
                data_uri = get_data_uri(image_bytes, ref_img.filename)
                img_dict = {"uri": data_uri}
                if tag:
                    img_dict["tag"] = tag
                reference_images.append(img_dict)

        # Create the text-to-image task using the SDK
        task = client.text_to_image.create(
            model=model,
            ratio=ratio,
            prompt_text=prompt_text,
            reference_images=reference_images  # Always pass the array, even if empty
        ).wait_for_task_output()

        # Extract the generated image URL from the task output
        if hasattr(task, 'output') and task.output:
            # The exact structure depends on the SDK response
            if isinstance(task.output, list) and len(task.output) > 0:
                image_url = task.output[0].get('image') or task.output[0].get('url')
            else:
                image_url = task.output.get('image') or task.output.get('url')
        else:
            image_url = None

        if image_url:
            return GenerateImageResponse(success=True, image_url=image_url)
        else:
            return GenerateImageResponse(success=False, error="No image URL in response")

    except TaskFailedError as e:
        return GenerateImageResponse(
            success=False,
            error=f"Runway task failed: {e.task_details}"
        )
    except Exception as e:
        return GenerateImageResponse(success=False, error=str(e))

@app.post("/generateimage-url", response_model=GenerateImageResponse)
async def generate_image_with_urls(request: GenerateImageURLRequest):
    """
    Generate image using URL-based reference images
    """
    try:
        # Initialize RunwayML client with API key
        runway_api_key = os.getenv("RUNWAYML_API_SECRET")
        if not runway_api_key:
            raise HTTPException(status_code=500, detail="Runway API key not configured")
        client = RunwayML(api_key=runway_api_key)
        
        # Prepare reference images from URLs
        reference_images = []
        if request.reference_images:
            for ref in request.reference_images:
                img_dict = {"uri": ref.url}  # Use URL directly as URI
                if ref.tag:
                    img_dict["tag"] = ref.tag
                reference_images.append(img_dict)

        # Create the text-to-image task using the SDK
        task = client.text_to_image.create(
            model=request.model,
            ratio=request.ratio,
            prompt_text=request.prompt_text,
            reference_images=reference_images  # Always pass the array, even if empty
        ).wait_for_task_output()

        # Extract the generated image URL from the task output
        if hasattr(task, 'output') and task.output:
            # The exact structure depends on the SDK response
            if isinstance(task.output, list) and len(task.output) > 0:
                image_url = task.output[0].get('image') or task.output[0].get('url')
            else:
                image_url = task.output.get('image') or task.output.get('url')
        else:
            image_url = None

        if image_url:
            return GenerateImageResponse(success=True, image_url=image_url)
        else:
            return GenerateImageResponse(success=False, error="No image URL in response")

    except TaskFailedError as e:
        return GenerateImageResponse(
            success=False,
            error=f"Runway task failed: {e.task_details}"
        )
    except Exception as e:
        return GenerateImageResponse(success=False, error=str(e))

@app.post("/generateimage-json", response_model=GenerateImageResponse)
async def generate_image_json(request: GenerateImageRequest):
    try:
        # Initialize RunwayML client with API key
        runway_api_key = os.getenv("RUNWAYML_API_SECRET")
        if not runway_api_key:
            raise HTTPException(status_code=500, detail="Runway API key not configured")
        client = RunwayML(api_key=runway_api_key)
        
        # Prepare reference images as data URIs with tags
        reference_images = []
        if request.reference_images:
            for ref in request.reference_images:
                # ref.base64_image is just base64, not a data URI
                image_bytes = base64.b64decode(ref.base64_image)
                data_uri = get_data_uri(image_bytes, ref.filename)
                img_dict = {"uri": data_uri}
                if ref.tag:
                    img_dict["tag"] = ref.tag
                reference_images.append(img_dict)

        # Create the text-to-image task using the SDK
        task = client.text_to_image.create(
            model=request.model,
            ratio=request.ratio,
            prompt_text=request.prompt_text,
            reference_images=reference_images  # Always pass the array, even if empty
        ).wait_for_task_output()

        # Extract the generated image URL from the task output
        if hasattr(task, 'output') and task.output:
            # The exact structure depends on the SDK response
            if isinstance(task.output, list) and len(task.output) > 0:
                image_url = task.output[0].get('image') or task.output[0].get('url')
            else:
                image_url = task.output.get('image') or task.output.get('url')
        else:
            image_url = None

        if image_url:
            return GenerateImageResponse(success=True, image_url=image_url)
        else:
            return GenerateImageResponse(success=False, error="No image URL in response")

    except TaskFailedError as e:
        return GenerateImageResponse(
            success=False,
            error=f"Runway task failed: {e.task_details}"
        )
    except Exception as e:
        return GenerateImageResponse(success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    
    parser = argparse.
    
    uvicorn.run(app, host="0.0.0.0", port=8000)