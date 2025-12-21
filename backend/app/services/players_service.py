from neo4j import Session
from app.db.repositories.players_repo import run_get_players_by_search_string

def get_player_by_search_string(session: Session, search_string: str):
  """
  The get_player_by_search_string service function calls the repository to get players with
  names matching the search string, and return the results in JSON format
  
  :param session: Neo4j Database session
  :type session: Session
  :param search_string: string to match against player full names (treated as a prefix)
  :type search_string: str
  """
  return {"results": run_get_players_by_search_string(session=session,
                                                      search_string=search_string)}