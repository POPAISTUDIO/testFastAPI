# FastAPI Image Generation Service

A FastAPI application that generates images using the Runway API. The service accepts text prompts and optional reference images to create custom images.

## Features

- **Image Generation**: Generate images from text prompts using Runway's AI
- **Reference Images**: Support for up to 3 reference images to guide generation
- **Multiple Endpoints**: Both file upload and JSON payload endpoints
- **Error Handling**: Comprehensive error handling and validation
- **Health Checks**: Built-in health monitoring endpoints

## Setup

### Prerequisites

- Python 3.8+
- Runway API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd testFastAPI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your Runway API key
```

4. Add your Runway API key to the `.env` file:
```
RUNWAYML_API_SECRET=your_actual_runway_api_key_here
```

## Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/health`
- Returns the health status of the service

### 2. Generate Image (File Upload)
- **POST** `/generateimage`
- Accepts multipart form data with:
  - `prompt` (required): Text description of the image to generate
  - `reference_image_1` (optional): First reference image file
  - `reference_image_2` (optional): Second reference image file
  - `reference_image_3` (optional): Third reference image file

### 3. Generate Image (JSON)
- **POST** `/generateimage-json`
- Accepts JSON payload with:
  - `prompt` (required): Text description of the image to generate
  - `reference_images` (optional): Array of base64 encoded images

## Usage Examples

### Using cURL with File Upload
```bash
curl -X POST "http://localhost:8000/generateimage" \
  -F "prompt=A beautiful sunset over mountains" \
  -F "reference_image_1=@path/to/reference1.jpg" \
  -F "reference_image_2=@path/to/reference2.jpg"
```

### Using cURL with JSON
```bash
curl -X POST "http://localhost:8000/generateimage-json" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape with flying cars",
    "reference_images": ["base64_encoded_image_1", "base64_encoded_image_2"]
  }'
```

### Using Python
```python
import httpx
import base64

# With file upload
async with httpx.AsyncClient() as client:
    with open("reference.jpg", "rb") as f:
        response = await client.post(
            "http://localhost:8000/generateimage",
            data={"prompt": "A beautiful landscape"},
            files={"reference_image_1": f}
        )
    print(response.json())

# With JSON payload
image_data = open("reference.jpg", "rb").read()
image_base64 = base64.b64encode(image_data).decode('utf-8')

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/generateimage-json",
        json={
            "prompt": "A beautiful landscape",
            "reference_images": [image_base64]
        }
    )
    print(response.json())
```

## Response Format

All endpoints return JSON responses in the following format:

```json
{
  "success": true,
  "image_url": "https://example.com/generated-image.jpg",
  "error": null
}
```

Or in case of an error:

```json
{
  "success": false,
  "image_url": null,
  "error": "Error message describing what went wrong"
}
```

## Testing

Run the test client to verify the API is working:

```bash
python test_client.py
```

## Configuration

The application can be configured through environment variables:

- `RUNWAYML_API_SECRET`: Your Runway API key (required)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes

- The Runway API endpoint URL in the code may need to be updated based on Runway's current API documentation
- Reference images should be in JPEG, PNG, or WEBP format
- Generated images are typically 1024x1024 pixels by default
- The API has a 60-second timeout for image generation requests

## Troubleshooting

1. **API Key Error**: Ensure your `RUNWAYML_API_SECRET` is correctly set in the `.env` file
2. **Connection Errors**: Check that the Runway API endpoint URL is correct and accessible
3. **Image Format Errors**: Ensure reference images are in supported formats (JPEG, PNG, WEBP)
4. **Timeout Errors**: Image generation can take time; consider increasing the timeout if needed