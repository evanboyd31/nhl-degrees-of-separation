import httpx
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
URI = os.getenv("PROD_NEO4J_URI" if ENVIRONMENT == "production" else "LOCAL_NEO4J_URI")
AUTH = (os.getenv("PROD_NEO4J_USERNAME" if ENVIRONMENT == "production" else "LOCAL_NEO4J_USERNAME"), 
        os.getenv("PROD_NEO4J_PASSWORD" if ENVIRONMENT == "production" else "LOCAL_NEO4J_PASSWORD"))

ALL_TEAMS_API_URL="https://api.nhle.com/stats/rest/en/team"

def get_teams() -> list:
  """
  The get_teams function returns a list of dicts of all historical NHL teams
  """
  teams = httpx.get(ALL_TEAMS_API_URL).json().get("data", [])
  return teams

def main() -> None:
  """
  The main function calls the get_teams() function, and then creates a Team
  node in the Neo4j database for each team
  """

  # get a list of Team JSONs from the NHL API
  teams = get_teams()
  
  # define a single driver to be used in the loop below for creating teams
  driver = GraphDatabase.driver(uri=URI, 
                                auth=AUTH)
  
  # use a merge query so that we don't create a bunch of duplicated teams in the event that we need to rerun
  # also define the string outside the loop for efficiency
  create_team_query = """
  MERGE (t:Team {id: $team_id})
  SET t.full_name = $team_full_name,
      t.tricode = $team_tricode
  """

  for team in teams:
    # a team is identified by its id, full name, and tricode (e.g., MTL)
    team_id = team.get("id")
    team_full_name = team.get("fullName")
    team_tricode = team.get("triCode")
    
    with driver.session() as session:
      session.run(create_team_query,
                  team_id=team_id,
                  team_full_name=team_full_name,
                  team_tricode=team_tricode)
      
      print(f"Inserted ${team_full_name} (ID: ${team_id}, tricode: ${team_tricode})")

  # always make sure to close the driver!
  driver.close()

if __name__ == "__main__":
  main()