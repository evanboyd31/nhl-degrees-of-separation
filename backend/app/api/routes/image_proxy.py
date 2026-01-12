from fastapi import APIRouter
from app.services.image_proxy import get_image_from_url

router = APIRouter(prefix="/image-proxy")

@router.get("/")
async def image_proxy(image_url: str):
  """
  The GET /image-proxy/ endpoint allows for images 
  from the NHL API to be rendered in the React
  frontend, as there are CORS policy errors otherwise
  
  :param image_url: The URL of the asset
  :type image_url: str
  """
  return await get_image_from_url(image_url=image_url)