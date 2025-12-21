from neo4j import Session

def run_get_players_by_search_string(session: Session, search_string: str):
  """
  The run_get_players_by_search_string executes a query on the Neo4j database
  to get the players matching the given search string

  :param session: Neo4j DB session
  :type session: Session
  :param search_string: string to match against player full names (treated as a prefix)
  :type search_string: str
  """

  search_for_player_query = """
  MATCH (p:Player)
  WHERE toLower(p.full_name) STARTS WITH toLower($search_string)
  RETURN p as player
  """

  result = session.run(search_for_player_query,
                       search_string=search_string)
  
  return [record.data().get("player") for record in result]