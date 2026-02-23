import React from "react";

interface Props {
  onClick: () => void;
}

const RandomPlayersButton: React.FC<Props> = ({ onClick }) => {
  return (
    <span>
      Pick Random Players <button onClick={onClick}>🔀</button>
    </span>
  );
};

export default RandomPlayersButton;
