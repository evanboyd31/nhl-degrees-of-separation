from typing import Any, Generator
from neo4j import GraphDatabase, Session
from .config import settings

# construct the neo4j connection info from the environemnt variables in config.py
neo4j_uri = settings.prod_neo4j_uri if settings.environment == "production" else settings.local_neo4j_uri
neo4j_username = settings.prod_neo4j_username if settings.environment == "production" else settings.local_neo4j_username
neo4j_password = settings.prod_neo4j_password if settings.environment == "production" else settings.local_neo4j_password
neo4j_auth = (neo4j_username, neo4j_password)

driver = GraphDatabase.driver(uri=neo4j_uri, auth=neo4j_auth)

def get_session() -> Generator[Session, Any, None]:
  """
  The get_session provides a uniform interface for the backend to perform queries on the database
  
  :return: a new session to execute Cypher queries
  :rtype: Generator[Session, Any, None]
  """
  with driver.session() as session:
    yield session