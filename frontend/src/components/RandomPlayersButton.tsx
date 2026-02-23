import React from "react";
import { Button } from "@mui/material";

interface Props {
  onClick: () => void;
}

const RandomPlayersButton: React.FC<Props> = ({ onClick }) => {
  return (
    <Button
      variant="outlined"
      onClick={onClick}
      sx={{
        color: "#ffffff",
        borderColor: "#ffffff",
        borderWidth: "2px",
        "&:hover": {
          borderWidth: "2px",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderColor: "#ffffff",
        },
        borderRadius: "20px",
        textTransform: "none",
      }}
    >
      Pick Random Players 🔀
    </Button>
  );
};

export default RandomPlayersButton;
