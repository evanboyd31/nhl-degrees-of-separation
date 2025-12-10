from neo4j import Session

def run_health_check_query(session: Session) -> dict | None:
  health_check_query = """
  MATCH (t:Team)
  WHERE t.tricode = "MTL"
  RETURN t
  """

  result = session.run(health_check_query)
  
  first_team = result.single()
  if first_team:
    return dict(first_team["t"])
  else:
    return None