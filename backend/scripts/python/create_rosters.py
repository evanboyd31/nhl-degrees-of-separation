import httpx
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
URI = os.getenv("PROD_NEO4J_URI" if ENVIRONMENT == "production" else "LOCAL_NEO4J_URI")
AUTH = (os.getenv("PROD_NEO4J_USERNAME" if ENVIRONMENT == "production" else "LOCAL_NEO4J_USERNAME"), 
        os.getenv("PROD_NEO4J_PASSWORD" if ENVIRONMENT == "production" else "LOCAL_NEO4J_PASSWORD"))

driver = GraphDatabase.driver(uri=URI,
                              auth=AUTH)

def get_team_seasons() -> list[dict]:
  """
  The get_team_seasons function returns a list of every NHL team's TeamSeason nodes from the Neo4j DB
  
  :return: List of TeamSeasons as well as Team nodes (e.g., [{"team" : {...}, "team_season": {...}}, ...])
  :rtype: list[dict]
  """

  # get the team as well because we need the team tricode
  get_team_seasons_query = """
  MATCH (team_season:TeamSeason)-[:SEASON_FOR]->(team:Team)
  RETURN team, team_season
  ORDER BY team.tricode
  """

  with driver.session() as session:
    result = session.run(get_team_seasons_query)
    rows = [record.data() for record in result]
    return rows

def main() -> None:
  team_seasons = get_team_seasons()


if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()