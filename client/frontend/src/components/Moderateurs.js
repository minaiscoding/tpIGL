import React from "react";
import Moderateur from "./Moderateur";

function Moderateurs({ moderateurs }) {
  return (
    <div>
      {moderateurs.map((moderateur) => (
        <Moderateur key={moderateur.nom} moderateur={moderateur} />
      ))}
    </div>
  );
}

export default Moderateurs;
