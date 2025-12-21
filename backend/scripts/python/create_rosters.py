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

TEAM_GAME_TYPES_BASE_API_URL = "https://api-web.nhle.com/v1/club-stats-season/"

def get_team_seasons() -> list[dict]:
  """
  The get_team_seasons function returns a list of every NHL team's TeamSeason nodes from the Neo4j DB
  
  :return: List of TeamSeasons as well as Team nodes (e.g., [{"team" : {...}, "team_season": {...}}, ...])
  :rtype: list[dict]
  """

  # get the team as well because we need the team tricode
  get_team_seasons_query = """
  MATCH (team_season:TeamSeason)-[:SEASON_FOR]->(team:Team)
  WHERE team.full_name CONTAINS "Canucks"
  RETURN team, team_season
  ORDER BY team.tricode
  """

  with driver.session() as session:
    result = session.run(get_team_seasons_query)
    rows = [record.data() for record in result]
    return rows
  
def get_team_game_types_for_seasons(tricode: str) -> list[dict]:
  """
  The get_game_types_for_season function returns a list of the type of 
  games that a given team played in during their seasons (2 = regular season,
  3 = playoffs). Used for minimizing API calls to the NHL API
  
  :param tricode: 3 letter tricode for the NHL team (e.g., "MTL")
  :type tricode: str
  :return: a list of game types that the team played during each of their seasons (will either be [2] or [2, 3])
  :rtype: list[int]
  """

  team_game_types_for_seasons = httpx.get(f"{TEAM_GAME_TYPES_BASE_API_URL}{tricode}").json()
  return team_game_types_for_seasons

def update_game_types(game_types: dict, tricode: str, game_types_for_seasons: list[dict]) -> None:
  """
  The function update_game_types updates the game_types caching dictionary to map tricode -> season -> game_types
  for each team season. Minimizes lookup time by using a dictionary rather than a list
  
  :param game_types: stores tricode -> season -> game_types entries
  :type game_types: dict
  :param tricode: tricode for an NHL team
  :type tricode: str
  :param game_types_for_seasons: a list of {"season", "gameTypes"} dictionary indicating the type of games the team played in, in each season
  :type game_types_for_seasons: list[dict]
  """
  
  game_types[tricode] = {}

  for season_game_type in game_types_for_seasons:
    season_id = season_game_type.get("season")
    season_game_types = season_game_type.get("gameTypes")
    game_types[tricode][season_id] = season_game_types

def main() -> None:
  seasons = get_team_seasons()

  # stores the types of games that a team played in during their seasons
  game_types = {}

  for season in seasons:
    team = season.get("team")
    team_season = season.get("team_season")

    tricode = team.get("tricode")
    season_id = team_season.get("id")[2:]

    # update the game type caching dictionary if necessary
    if game_types.get(tricode, None) is None:
      game_types_for_seasons = get_team_game_types_for_seasons(tricode=tricode)
      update_game_types(game_types=game_types,
                        tricode=tricode,
                        game_types_for_seasons=game_types_for_seasons)
      
    game_types_for_season = game_types.get(tricode).get(season_id)




if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()