from app.db.repositories.health_check_repo import run_health_check_query

def run_health_check(session):
  return {"status": "ok", 
          "healthCheckQueryResult": run_health_check_query(session=session)}