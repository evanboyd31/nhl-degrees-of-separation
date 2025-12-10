from fastapi import APIRouter, Depends
from app.core.neo4j import get_session
from app.services.health_check_service import run_health_check

router = APIRouter(prefix="/health-check")

@router.get("/")
def health_check(session = Depends(get_session)):
  return run_health_check(session)