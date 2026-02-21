# NHL Degrees of Separation 🕸️🏒

An interactive discovery engine that finds the connection between every NHL player ever using shared teammates.

## Introduction

Every era of the NHL is distinct, but every player is connected. Inspired by Wayne Gretzky's book "99: Stories of the Game", I built this graph-based search engine to discover the connections between every player to ever play in the NHL from 1917 to present day.

## View Online

The NHL Degrees of Separation web application can be viewed [here](https://nhl-degrees-of-separation-frontend.onrender.com/).

## Design

### Data Model & Schema

The Neo4j node labels are the following:

- Nodes:
  - `Player`: Represents a player that has played in the NHL (e.g., Nick Suzuki).
  - `TeamSeason`: Represents a team (or roster) in a specific year (e.g., the 2025-2026 Montreal Canadiens)
  - `Team`: An NHL franchise (e.g., the Montreal Canadiens)

- Relationships:
  - `(Player)-[:PLAYED_FOR]->(TeamSeason)`: Connects a player to a specific roster (e.g., `(Nick Suzuki)-[:PLAYED_FOR]->(2025-2026 Montreal Canadiens)`)
  - `(TeamSeason)-[:SEASON_FOR]->(Team)`: Connects a team's season to the parent franchise (e.g., `(2025-2026 Montreal Canadiens)-[:SEASON_FOR]->(Montreal Canadiens)`)

### Path Finding Algorithm

The path finding algorithm leverages Neo4j's builtin `shortestPath` function, which implements a Breadth-First Search (BFS) to guarantee the shortest path between two players.

Players are not linked directly to each other as this would create an extremely dense and memory inefficient graph; they are connected through intermediary `TeamSeason` nodes, which encapsulate rosters. A path between two follows the pattern:

```
(Player_A)-[:PLAYED_FOR]->(TeamSeason_1)<-[:PLAYED_FOR]-(Player_B)-[:PLAYED_FOR]->...
```

The backend executes a query of the form to find the degrees of separation:

```
MATCH (Player_A:Player {id: $id1}), (Player_N:Player {id: $id2})
MATCH path = shortestPath((p1)-[:PLAYED_FOR*..30]-(p2))
RETURN path
```

Note that a depth constraint of at most 30 nodes is used to prevent long-running queries, as most NHL players are separated by less than 6 degrees.

### Limitations

## Technologies Used

<p align="center"> 
  <img src="https://images.seeklogo.com/logo-png/53/3/fastapi-framework-logo-png_seeklogo-535865.png" alt="FastAPI Logo" width="100" style="margin: 0 15px;"/> 
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" alt="React Logo" width="100" style="margin: 0 15px;"/> 
  <img src="https://assets.streamlinehq.com/image/private/w_300,h_300,ar_1/f_auto/v1/icons/4/neo4j-scjhzfu70ksd2paadypqr.png/neo4j-do4n8gc78dqpmorqrg1qt8.png?_a=DATAiZAAZAA0" alt="Neo4j Logo" width="100" style="margin: 0 15px;"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" alt="Docker Logo" width="100" style="margin: 0 15px;"/> 
</p>

## License

All rights reserved. The code and content of this repository cannot be used, modified, or distributed without explicit permission from the author.
