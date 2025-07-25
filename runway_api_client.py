"""
Runway API Client for image generation
"""
import httpx
import os
import base64
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class RunwayAPIClient:
    def __init__(self):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        if not self.api_key:
            raise ValueError("RUNWAY_API_KEY environment variable is required")
        
        # Base URL for Runway API
        self.base_url = "https://api.runwayml.com/v1"
        self.timeout = 60.0
    
    async def generate_image(
        self,
        prompt: str,
        reference_images: Optional[List[str]] = None,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50
    ) -> Dict[str, Any]:
        """
        Generate an image using Runway's API
        
        Args:
            prompt: Text description of the image to generate
            reference_images: List of base64 encoded reference images
            width: Image width
            height: Image height
            num_images: Number of images to generate
            guidance_scale: Guidance scale for generation
            num_inference_steps: Number of inference steps
            
        Returns:
            Dictionary containing the API response
        """
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_images": num_images,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps
        }
        
        # Add reference images if provided
        if reference_images:
            payload["reference_images"] = reference_images
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/inference",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                raise Exception(f"Runway API error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Request error: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
    
    def validate_image_format(self, image_data: bytes) -> bool:
        """
        Validate that the image data is in a supported format
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            True if valid, False otherwise
        """
        try:
            from PIL import Image
            from io import BytesIO
            
            image = Image.open(BytesIO(image_data))
            # Check if format is supported (JPEG, PNG, etc.)
            return image.format in ['JPEG', 'PNG', 'WEBP']
        except Exception:
            return False
    
    def encode_image(self, image_data: bytes) -> str:
        """
        Encode image data to base64
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_data).decode('utf-8') 