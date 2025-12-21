from fastapi import APIRouter, Depends
from app.core.neo4j import get_session
from app.services.players_service import get_player_by_search_string

router = APIRouter(prefix="/players")

@router.get("/search/")
def search_for_player(session = Depends(get_session), search_string: str = ""):
  """
  The GET /players/search/ endpoint allows the user to search for a player by a search_string prefix
  
  :param session: Neo4j DB Session dependency
  :param search_string: string to match against player full names (treated as a prefix)
  :type search_string: str
  """
  return get_player_by_search_string(session=session, 
                                     search_string=search_string)