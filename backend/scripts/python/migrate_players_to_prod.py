from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
from itertools import islice

load_dotenv()

LOCAL_URI = os.getenv("LOCAL_NEO4J_URI")
LOCAL_AUTH = (os.getenv("LOCAL_NEO4J_USERNAME"), 
              os.getenv("LOCAL_NEO4J_PASSWORD"))
local_driver = GraphDatabase.driver(uri=LOCAL_URI, 
                                    auth=LOCAL_AUTH)

PROD_URI = os.getenv("PROD_NEO4J_URI")
PROD_AUTH = (os.getenv("PROD_NEO4J_USERNAME"), 
             os.getenv("PROD_NEO4J_PASSWORD"))
prod_driver = GraphDatabase.driver(uri=PROD_URI, 
                                   auth=PROD_AUTH)

def get_local_played_for_relationships() -> list[dict]:
  """
  The get_local_played_for_relationships function gets a list of the Player,
  TeamSeason nodes participating in PLAYED_FOR relationships in the local
  Neo4j database
  """

  get_played_for_relationship_query = """
  MATCH (p:Player)-[pf:PLAYED_FOR]->(ts:TeamSeason)
  RETURN p, pf, ts
  ORDER BY ts.id, p.id
  """

  with local_driver.session() as session:
    result = session.run(query=get_played_for_relationship_query)

    rows = []

    for record in result:
      player = record["player"]
      player_attrs = dict(player.items())
      
      played_for = record["pf"]
      player_for_attrs = dict(played_for.items())

      team_season = record["ts"]
      team_season_attrs = dict(team_season.items())

      played_for_relationship = {
        "player_id": player_attrs.get("id"),
        "player_attrs": player_attrs,

        "ts_id": team_season_attrs.get("id"),
        "team_season_attrs": team_season_attrs,

        "played_for_attrs": player_for_attrs
      }

      rows.append(played_for_relationship)

    return rows


def main() -> None:
  played_for_relationships = get_local_played_for_relationships()

if __name__ == "__main__":
  try:
    main()
  finally:
    local_driver.close()
    prod_driver.close()
