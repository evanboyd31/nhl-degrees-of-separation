import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  environment: str = os.getenv("ENVIRONMENT", "local")

  prod_neo4j_uri: str | None = os.getenv("PROD_NEO4J_URI")
  prod_neo4j_username: str | None = os.getenv("PROD_NEO4J_USERNAME")
  prod_neo4j_password: str| None = os.getenv("PROD_NEO4J_PASSWORD")

  local_neo4j_uri: str | None = os.getenv("LOCAL_NEO4J_URI")
  local_neo4j_username: str | None = os.getenv("LOCAL_NEO4J_USERNAME")
  local_neo4j_password: str| None = os.getenv("LOCAL_NEO4J_PASSWORD")

settings = Settings()