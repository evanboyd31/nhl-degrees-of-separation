from fastapi import FastAPI
from app.api.routes import health_check
from app.api.routes import players

app = FastAPI(title="NHL Degrees of Separation")

# health check routes
app.include_router(health_check.router)

# player routes
app.include_router(players.router)