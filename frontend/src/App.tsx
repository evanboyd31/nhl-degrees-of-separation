import { useState, useEffect } from "react";
import PlayerSearchHeader from "./components/PlayerSearchHeader";
import ShortestPathGraph from "./components/ShortestPathGraph";
import {
  getShortestPathBetweenTwoPlayers,
  getShortestPathBetweenTwoRandomPlayers,
} from "./api/nhlAPI";
import { CircularProgress } from "@mui/material";
import { type Player } from "./types/nhl";
import "./styles/global.css";
import Footer from "./components/Footer";

const App = () => {
  const [player1, setPlayer1] = useState<Player | null>(null);
  const [player2, setPlayer2] = useState<Player | null>(null);
  const [shortestPath, setShortestPath] = useState([]);
  const [loadingPath, setLoadingPath] = useState<Boolean>(false);

  useEffect(() => {
    /**
     * The getShortestPath function will update the displayed shortest path everytime
     * two new players (player1 and player2 state vars) are selected in the dropdown
     */
    const getShortestPath = async () => {
      // only call shortest path endpoint if two players have been selected
      if (player1 && player2) {
        setLoadingPath(true);
        const player1Id = player1.id;
        const player2Id = player2.id;
        const shortestPathResponse = await getShortestPathBetweenTwoPlayers(
          player1Id,
          player2Id,
        );
        setShortestPath(shortestPathResponse);
        setLoadingPath(false);
      }
    };

    getShortestPath();
  }, [player1, player2]);

  const onRandomClick = async () => {
    setLoadingPath(true);
    const randomPlayerPathResponse =
      await getShortestPathBetweenTwoRandomPlayers();
    setShortestPath(randomPlayerPathResponse);
    setLoadingPath(false);
  };

  return (
    <div>
      <PlayerSearchHeader
        label1="Player 1 (Enter to Search)"
        label2="Player 2 (Enter to Search)"
        onSelect1={setPlayer1}
        onSelect2={setPlayer2}
        onRandomClick={onRandomClick}
      />

      <main className="main-content">
        {loadingPath && <CircularProgress />}
        {shortestPath.length !== 0 ? (
          <ShortestPathGraph pathData={shortestPath} />
        ) : (
          <div className="help-text">
            Discover how any two NHL players are connected through teammates.
            Search for two players to begin.
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default App;
