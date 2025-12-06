from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

with GraphDatabase.driver(URI, auth=AUTH) as driver:
  driver.verify_connectivity()

  summary = driver.execute_query("""
    CREATE (a:Person {name: $name})
    CREATE (b:Person {name: $friendName})
    CREATE (a)-[:KNOWS]->(b)
    """,
    name="Alice", friendName="David",
    database_="neo4j",
  ).summary

  print("Created {nodes_created} nodes in {time} ms.".format(
      nodes_created=summary.counters.nodes_created,
      time=summary.result_available_after
  ))