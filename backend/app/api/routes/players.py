from fastapi import APIRouter, Depends
from app.core.neo4j import get_session
from app.services.players_service import get_player_by_search_string, get_shortest_path, get_random_shortest_path

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

@router.get("/shortest-path/")
def find_shortest_path_between_two_players(player_1_id: int, player_2_id: int, session = Depends(get_session)):
  """
  Docstring for find_shortest_path_between_two_players
  
  :param player_1_id: The NHL API id of the first player
  :type player_1_id: int
  :param player_2_id: The NHL API id of the second player
  :type player_2_id: int
  :param session: Neo4j DB Session dependency
  """

  return get_shortest_path(session=session,
                           player_1_id=player_1_id,
                           player_2_id=player_2_id)

@router.get("/random-shortest-path/")
def find_shortest_path_between_two_random_players(session = Depends(get_session)):
  """
  The GET /random-shortest-path/ endpoint allows the user to search for an example 
  shortest path between two randomized NHL players
  
  :param session: Neo4j DB Session dependency
  """

  return get_random_shortest_path(session=session)
