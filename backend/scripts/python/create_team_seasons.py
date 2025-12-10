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

def get_teams_tricodes() -> list:
  """
  The get_teams_tricodes function returns a list of the 3 letter tricodes of all historical NHL teams (e.g., ["MTL", "VAN", ...])
  """

  get_team_abbreviations_query = """
  MATCH (t:Team)
  RETURN t.tricode
  """

  with driver.session() as session:
    result = session.run(get_team_abbreviations_query)
    return [record.value() for record in result]

def main() -> None:

  print(get_teams_tricodes())

if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()