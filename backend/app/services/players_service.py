from neo4j import Session
from app.db.repositories.players_repo import run_get_players_by_search_string, run_get_shortest_path_between_two_players

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

def get_shortest_path(session: Session, player_1_id: int, player_2_id: int):
  """
  The get_shortest_path service function calls the repository to find the
  shortest path between two NHL players, and return the results in JSON format
  
  :param session: Neo4j Database session
  :type session: Session
  :param player_1_id: The NHL API id of the first player
  :type player_1_id: int
  :param player_2_id: The NHL API id of the second player
  :type player_2_id: int
  """

  shortest_path_results = run_get_shortest_path_between_two_players(session=session,
                                                                    player_1_id=player_1_id,
                                                                    player_2_id=player_2_id)
  
  hops = shortest_path_results[0].get("hops")
  nodes = shortest_path_results[0].get("node_attrs")
  relationships = shortest_path_results[0].get("relationship_attrs")
  response = []

  # handle case where no path exists
  if not relationships:
    return {"results": {"hops": hops, "path": []}}

  # iterate over all nodes and add the most recent headshot to each player in the path
  for node_index, node in enumerate(nodes):
    if "position_code" in node:
      if node_index == 0:
        relationship = relationships[0]
      else:
        relationship = relationships[node_index - 1]

      node["headshot_url"] = relationship.get("headshot_url")
    response.append(node)

  return {"results": {"hops": hops, "path": response}}