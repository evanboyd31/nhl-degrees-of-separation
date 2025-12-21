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
  ORDER BY p.full_name
  """

  result = session.run(search_for_player_query,
                       search_string=search_string)
  
  return [record.data().get("player") for record in result]


def run_get_shortest_path_between_two_players(session: Session, player_1_id: int, player_2_id: int):
  """
  The run_get_shortest_path_between_two_players executes the shortest path query between two players
  
  :param session: Neo4j DB session
  :type session: Session
  :param player_1_id: The NHL API id of the first player
  :type player_1_id: int
  :param player_2_id: The NHL API id of the second player
  :type player_2_id: int
  """

  shortest_path_query = """
  MATCH (p1:Player {id: $player_1_id})
  MATCH (p2:Player {id: $player_2_id})
  MATCH path = shortestPath( (p1)-[:PLAYED_FOR*..30]-(p2) )
  RETURN
    length(path) AS hops,
    [r IN relationships(path) | properties(r)] AS relationship_attrs,
    [n IN nodes(path) | properties(n)] AS node_attrs
  """

  result = session.run(shortest_path_query,
                       player_1_id=player_1_id,
                       player_2_id=player_2_id)

  return [record.data() for record in result]