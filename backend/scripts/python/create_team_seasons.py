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

def get_team_seasons(tricode: str) -> list[int]:
  """
  Given a team's tricode, get the seasons that the team played in
  
  :param tricode: tricode for an NHL team (unique)
  :type tricode: str
  :return: list of season IDs that the team played in (e.g., [19191920, 19201921, ..., 20252026])
  :rtype: list[int]
  """
  team_seasons = httpx.get(f"{TEAM_SEASONS_BASE_API_URL}{tricode}").json()
  return team_seasons

def get_team_season_logo_url(tricode: str, season: int) -> str:
  """
  Given a team and a season, get the team's logo for that season
  
  :param tricode: Tricode for the NHL team (e.g., "MTL")
  :type tricode: str
  :param season: Season id (e.g., 20252026)
  :type season: int
  """

  # fetch the games for the team's season
  team_schedule_for_seasons = httpx.get(f"{TEAM_SCHEDULE_BASE_API_URL}{tricode}/{season}").json()
  games = team_schedule_for_seasons.get("games", [])

  if len(games) > 0:
    # get the first game of the year
    first_game = games[0]

    # check to see if the provided team was the home or away team to get correct logo
    home_team = first_game.get("homeTeam", {})
    away_team = first_game.get("awayTeam", {})

    logo_url = ""
    if home_team.get("abbrev", "") == tricode:
      logo_url = home_team.get("logo", "")
    else:
      logo_url = away_team.get("logo", "")

    return logo_url
  
def format_team_season_full_name(team_full_name: str, season: int) -> str:
  """
  The format_team_season_full_name provides the uniform format for TeamSeason full_name fields (e.g., "Montreal Canadiens (2025-2026)")
  
  :param team_full_name: Full name of the NHL team (e.g., "Montreal Canadiens")
  :type team_full_name: str
  :param season: Season id (e.g., 20252026)
  :type season: int
  :return: Formatted TeamSeason full_name (e.g., "Montreal Canadiens (2025-2026)")
  :rtype: str
  """
  return f"{team_full_name} ({str(season)[:4]}-{str(season)[4:]})"

def main() -> None:
  teams = get_teams()

  create_team_season_query = """
  MATCH (t: Team {id: $team_id})
  MERGE (ts: TeamSeason {id: $team_season_id})-[:SEASON_FOR]->(t)
  ON CREATE SET ts.full_name = $full_name,
                ts.logo_url = $logo_url
  """
  
  # for each team
  with driver.session() as session:
    for team in teams[:1]:

      # get the seasons they played in
      team_id = team.get("id")
      team_full_name = team.get("full_name")
      tricode = team.get("tricode", "")
      team_seasons = get_team_seasons(tricode=tricode)
      
      # for each season the team played in
      with session.begin_transaction() as tx:
        for season in team_seasons:

          # get their logo for that season and create a TeamSeason node in Neo4j DB
          logo_url = get_team_season_logo_url(tricode=tricode, 
                                              season=season)

          # ids for TeamSeasons will be of the form team_id-season, e.g., 1-20252026
          team_season_id = f"{team_id}-{season}"

          # format the name of the TeamSeason
          team_season_full_name = format_team_season_full_name(team_full_name=team_full_name,
                                                               season=season)      
          
          tx.run(create_team_season_query,
                 team_id=team_id,
                 team_season_id=team_season_id,
                 full_name=team_season_full_name,
                 logo_url=logo_url)
          
          print(f"Inserted ${team_season_id} (season: {season}, logo_url: {logo_url})")


if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()