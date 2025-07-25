#!/usr/bin/env python3
"""
Test client for the Image Generation API
"""
import asyncio
import httpx
import base64
from pathlib import Path

async def test_generate_image_with_files():
    """Test the /generateimage endpoint with file uploads"""
    url = "http://localhost:8000/generateimage"
    
    # Test data
    prompt = "A beautiful sunset over mountains with a lake in the foreground"
    
    # Prepare form data
    data = {"prompt": prompt}
    files = {}
    
    # Add reference images if they exist
    for i in range(1, 4):
        ref_path = Path(f"reference_image_{i}.jpg")
        if ref_path.exists():
            files[f"reference_image_{i}"] = open(ref_path, "rb")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
    finally:
        # Close any open files
        for file in files.values():
            if hasattr(file, 'close'):
                file.close()

async def test_generate_image_json():
    """Test the /generateimage-json endpoint with JSON payload"""
    url = "http://localhost:8000/generateimage-json"
    
    # Test data
    payload = {
        "prompt": "A futuristic cityscape with flying cars and neon lights",
        "reference_images": []  # Add base64 encoded images here if needed
    }
    
    # Example of how to add a reference image
    # with open("reference_image.jpg", "rb") as f:
    #     image_data = f.read()
    #     image_base64 = base64.b64encode(image_data).decode('utf-8')
    #     payload["reference_images"].append(image_base64)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

async def test_health_check():
    """Test the health check endpoint"""
    url = "http://localhost:8000/health"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Check Response: {response.json()}")

async def main():
    """Run all tests"""
    print("Testing Image Generation API...")
    print("=" * 50)
    
    # Test health check first
    print("\n1. Testing health check:")
    await test_health_check()
    
    # Test JSON endpoint
    print("\n2. Testing JSON endpoint:")
    await test_generate_image_json()
    
    # Test file upload endpoint
    print("\n3. Testing file upload endpoint:")
    await test_generate_image_with_files()

if __name__ == "__main__":
    asyncio.run(main()) 