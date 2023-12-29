import React from "react";
import Moderateur from "./Moderateur";

function Moderateurs({ moderateurs }) {
  return (
    <div className="flex flex-col  justify-start items-start h-full w-full">
      {moderateurs.map((moderateur) => (
        <Moderateur key={moderateur.nom} moderateur={moderateur} />
      ))}
    </div>
  );
}

export default Moderateurs;
