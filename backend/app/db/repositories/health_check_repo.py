from neo4j import Session

def run_health_check_query(session: Session) -> dict | None:
  health_check_query = """
  MERGE (hc:HealthCheck {service_name: $service_name})
  SET hc.last_check = datetime()
  RETURN hc
  """

  result = session.run(health_check_query,
                       service_name="health-check-id")
  
  health_check = result.single()
  if health_check:
    return dict(health_check["hc"])
  else:
    return None