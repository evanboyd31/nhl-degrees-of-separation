import React, { useState } from "react";
import { Autocomplete, TextField, CircularProgress } from "@mui/material";
import { getPlayersByName } from "../api/nhlAPI";
import { type Player } from "../types/nhl";

interface Props {
  label: string;
  onSelect: (player: Player | null) => void;
}

const PlayerSearchBar: React.FC<Props> = ({ label, onSelect }) => {
  const [textSearchValue, setTextSearchValue] = useState("");
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);

  /**
   * The handleKeyDown function updates state variables according to the keys
   * inputted to the Autocomplete component
   * @param event - keyboard event (the key entered)
   * @returns void function
   */
  const handleKeyDown = async (event: React.KeyboardEvent) => {
    // only update the list of players in the autocomplete when the user presses enter to reduce overfetching
    if (event.key === "Enter") {
      event.preventDefault();

      // only search for players when a non-empty string is provided
      if (textSearchValue) {
        setLoading(true);
        const playersResponse = await getPlayersByName(textSearchValue);
        setPlayers(playersResponse || []);
        setLoading(false);
      }
    }
  };

  return (
    <Autocomplete
      options={players}
      getOptionLabel={(option) => option.full_name || ""}
      inputValue={textSearchValue}
      onInputChange={(_, newTextSearchValue) => {
        setTextSearchValue(newTextSearchValue);
      }}
      onChange={(_, newValue: Player | null) => {
        onSelect(newValue);
      }}
      loading={loading}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          onKeyDown={handleKeyDown}
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <>
                {loading ? (
                  <CircularProgress color="inherit" size={20} />
                ) : null}
                {params.InputProps.endAdornment}
              </>
            ),
          }}
        />
      )}
      sx={{
        width: 400,
        "& .MuiOutlinedInput-root": {
          backgroundColor: "white",
          borderRadius: "4px",
        },
        boxShadow: "0px 2px 4px rgba(0,0,0,0.1)",
      }}
    />
  );
};

export default PlayerSearchBar;
