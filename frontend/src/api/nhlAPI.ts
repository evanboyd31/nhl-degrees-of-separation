import axios from "axios";
import { type Player } from "../types/nhl";

const API_URL = import.meta.env.VITE_BASE_API_URL;

/**
 * Given a searchString, return a list of NHL players whose full names prefix match the string
 * @param searchString the name of the player to search for
 * @returns a Promise that resolves to an array of Players, or an empty array if no players match the string or an error occurs
 */
export const getPlayersByName = async (
  searchString: string
): Promise<Player[]> => {
  try {
    const response = await axios.get(
      `${API_URL}players/search/?search_string=${searchString.toLowerCase()}`
    );
    return response.data.results || [];
  } catch (error) {
    return [];
  }
};

/**
 * The getShortestPathBetweenTwoPlayers function will return the shortest path connecting
 * two NHL players and the teams that they have played for
 * @param player1Id - NHL API id of the first player
 * @param player2Id - NHL API id of the second player
 * @returns an array representing the shortest Player - TeamSeason - Player - TeamSeason - ... - Player path
 */
export const getShortestPathBetweenTwoPlayers = async (
  player1Id: Number,
  player2Id: Number
) => {
  try {
    const response = await axios.get(
      `${API_URL}players/shortest-path/?player_1_id=${player1Id}&player_2_id=${player2Id}`
    );

    return response.data?.results?.path || [];
  } catch (error) {
    return [];
  }
};
