import React from "react";
import Moderateur from "./Moderateur";

function Moderateurs({ moderateurs, setModerateurs }) {
  return (
    <div className="flex flex-col  justify-start items-start h-full w-full">
      {moderateurs.map((moderateur) => (
        <Moderateur
          key={moderateur.id}
          moderateur={moderateur}
          setModerateurs={setModerateurs}
        />
      ))}
    </div>
  );
}

export default Moderateurs;
