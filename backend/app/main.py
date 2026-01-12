from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health_check
from app.api.routes import players
from app.api.routes import image_proxy

app = FastAPI(title="NHL Degrees of Separation")

# allowed CORS origins
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

# health check routes
app.include_router(health_check.router)

# player routes
app.include_router(players.router)

# image proxy routes
app.include_router(image_proxy.router)