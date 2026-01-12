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
