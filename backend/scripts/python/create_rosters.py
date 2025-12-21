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
# team roster example: https://api-web.nhle.com/v1/club-stats/TOR/20242025/3
TEAM_ROSTER_BASE_API_URL = "https://api-web.nhle.com/v1/club-stats/"


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
  ORDER BY team.tricode, team_season.id
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

def create_players_for_team_season(tricode: str, team_season_id: str, season_id: int, game_types_for_season: list[int]) -> None:
  """
  The create_players_for_team_season function performs the following logic: given a team and a season, create Neo4j nodes
  for each player on that team/season's roster
  
  :param tricode: tricode of the NHL team
  :type tricode: str
  :param team_season_id: TeamSeason node id in Neo4j (used for creating relationships, e.g., "1-20252026")
  :type team_season_id: str
  :param season_id: Season id of an NHL season (e.g., 20252026)
  :type season_id: int
  :param game_types_for_season: The game types that the team played in during the season (used for querying rosters, 2 = regular season, 3 = playoffs)
  :type game_types_for_season: list[int]
  """
  create_player_query = """
  MATCH (ts:TeamSeason {id: $team_season_id})
  MERGE (p:Player {id: $player_id})
  ON CREATE SET p.full_name = $full_name,
                p.position_code = $position_code
  MERGE (p)-[pf:PLAYED_FOR]->(ts)
  ON CREATE SET pf.headshot_url = $headshot_url
  ON MATCH  SET pf.headshot_url = $headshot_url
  """

  with driver.session() as session:
    for game_type in game_types_for_season:
      team_roster = httpx.get(f"{TEAM_ROSTER_BASE_API_URL}{tricode}/{season_id}/{game_type}").json()
      
      # get listers of skaters and goalies (position for goalies is "G", but is not provided in this endpoint)
      skaters = team_roster.get("skaters", [])
      goalies = team_roster.get("goalies", [])

      with session.begin_transaction() as tx:

        # create a Player node for each skater
        for skater in skaters:
          player_id = skater.get("playerId")
          full_name = f"{skater.get("firstName", {}).get("default", "")} {skater.get("lastName", {}).get("default", "")}"
          position_code = skater.get("positionCode", "")
          headshot_url = skater.get("headshot", "")

          tx.run(create_player_query,
                 team_season_id=team_season_id,
                 player_id=player_id,
                 full_name=full_name,
                 position_code=position_code,
                 headshot_url=headshot_url)
          
          print(f"Inserted/updated player {player_id} ({full_name}) for {tricode} {season_id}")

        # create a Player node for each goalie
        for goalie in goalies:
          player_id = goalie.get("playerId")
          full_name = f"{goalie.get("firstName", {}).get("default", "")} {goalie.get("lastName", {}).get("default", "")}"
          position_code = "G"
          headshot_url = goalie.get("headshot", "")

          tx.run(create_player_query,
                 team_season_id=team_season_id,
                 player_id=player_id,
                 full_name=full_name,
                 position_code=position_code,
                 headshot_url=headshot_url)
          
          print(f"Inserted/updated goalie {player_id} ({full_name}) for {tricode} {season_id}")


def main() -> None:
  seasons = get_team_seasons()

  # stores the types of games that a team played in during their seasons
  game_types = {}

  for season in seasons:
    team = season.get("team")
    team_season = season.get("team_season")

    tricode = team.get("tricode", "")
    team_season_id = team_season.get("id", "")
    # TeamSeason ids are of the form {team_id}-{season_id}
    season_id = int(team_season_id.split("-", 1)[1])

    # update the game type caching dictionary if necessary
    if game_types.get(tricode, None) is None:
      game_types_for_seasons = get_team_game_types_for_seasons(tricode=tricode)
      update_game_types(game_types=game_types,
                        tricode=tricode,
                        game_types_for_seasons=game_types_for_seasons)
      
    game_types_for_season = game_types.get(tricode).get(season_id)

    # create players in Neo4j for this team's roster for the current season
    create_players_for_team_season(tricode=tricode,
                                   team_season_id=team_season_id,
                                   season_id=season_id,
                                   game_types_for_season=game_types_for_season)


if __name__ == "__main__":
  main()

  # always make sure to close the driver!
  driver.close()