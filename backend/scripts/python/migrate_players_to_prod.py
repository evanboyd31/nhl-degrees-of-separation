from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()


LOCAL_URI = os.getenv("LOCAL_NEO4J_URI")
LOCAL_AUTH = (os.getenv("LOCAL_NEO4J_USERNAME"), 
              os.getenv("LOCAL_NEO4J_PASSWORD"))

local_driver = GraphDatabase.driver(uri=LOCAL_URI,
                                    auth=LOCAL_AUTH)

PROD_URI = os.getenv("PROD_NEO4J_URI")
PROD_AUTH = (os.getenv("PROD_NEO4J_USERNAME"), 
             os.getenv("PROD_NEO4J_PASSWORD"))

prod_driver = GraphDatabase.driver(uri=PROD_URI,
                                   auth=LOCAL_AUTH)