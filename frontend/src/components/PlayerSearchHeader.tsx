import { type Player } from "../types/nhl";
import PlayerSearchBar from "./PlayerSearchBar";
import "./PlayerSearchHeader.css";

interface Props {
  /** The default text label used in the Player 1 Autocomplete dropdown */
  label1: string;
  /** The default text label used in the Player 2 Autocomplete dropdown */
  label2: string;
  /** Callback function to update Player 1 from the first Autocomplete dropdown */
  onSelect1: (player: Player | null) => void;
  /** Callback function to update Player 2 from the first Autocomplete dropdown */
  onSelect2: (player: Player | null) => void;
}

/**
 * The PlayerSearchHeader component returns the header used at the top of the screen.
 * This header contains two search bars (one for each player) so the user can lookup
 * the connections between the two NHL players
 */
const PlayerSearchHeader: React.FC<Props> = ({
  label1,
  label2,
  onSelect1,
  onSelect2,
}) => {
  return (
    <header className="search-header">
      <div className="search-container">
        <PlayerSearchBar label={label1} onSelect={onSelect1} />
      </div>
      <div className="search-arrow">➔</div>
      <div className="search-container">
        <PlayerSearchBar label={label2} onSelect={onSelect2} />
      </div>
    </header>
  );
};

export default PlayerSearchHeader;
