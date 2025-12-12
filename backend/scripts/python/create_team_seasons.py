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

TEAM_SEASONS_BASE_API_URL = "https://api-web.nhle.com/v1/roster-season/"
TEAM_SCHEDULE_BASE_API_URL = "https://api-web.nhle.com/v1/club-schedule-season/"

def get_teams() -> list[str]:
  """
  The get_teams function returns a list of all NHL teams in the Neo4j DB
  
  :return: List of teams (e.g., [{"id": 1, "full_name": "Montreal Canadiens", "tricode": "MTL"}])
  :rtype: list[str]
  """

  get_teams_query = """
  MATCH (t:Team)
  RETURN t.id as id, t.full_name as full_name, t.tricode as tricode
  """

  with driver.session() as session:
    result = session.run(get_teams_query)
    return [{ "id": record["id"], "full_name": record["full_name"], "tricode": record["tricode"] } for record in result]

def main() -> None:
  teams = get_teams()
  print(teams)


if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()