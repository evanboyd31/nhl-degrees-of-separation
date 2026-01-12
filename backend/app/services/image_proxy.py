import httpx
from fastapi import HTTPException, Response
from urllib.parse import urlparse

ALLOWED_DOMAINS = ["assets.nhle.com"]

async def get_image_from_url(image_url: str) -> Response:
  """
  Fetches an image from the NHL assets DB and returns a FastAPI Response 
  with the correct media type to be streamed to the frontend.
  """

  # confirm that the image has an origin domain of assets.nhle.com (so this endpoint can't be used for other domains)
  parsed_url = urlparse(image_url)
  if parsed_url.netloc not in ALLOWED_DOMAINS:
    raise HTTPException(
      status_code=403, 
      detail=f"Proxying to domain {parsed_url.netloc} is forbidden."
    )

  async with httpx.AsyncClient() as client:
    try:
      headers = {"User-Agent": "Mozilla/5.0"}
      response = await client.get(image_url, headers=headers, follow_redirects=True)
          
      if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Could not fetch image")

      # Return a Response object with the raw bytes and correct Content-Type
      return Response(
        content=response.content,
        media_type=response.headers.get("Content-Type", "image/png")
      )
          
    except httpx.RequestError as exc:
      raise HTTPException(status_code=500, detail=f"Error contacting image server: {exc}")