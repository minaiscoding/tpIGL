import React from "react";
import { useState } from "react";
import iconUser from "../assets/iconUser.png";
import iconMdp from "../assets/iconMdp.png";
import iconEmail from "../assets/iconEmail.png";
function Moderateur(moderateur) {
  const [clicked, setClicked] = useState(false);
  const supprimer = () => {};
  const modifier = () => {};
  return (
    <div onClick={() => setClicked(!clicked)}>
      {clicked === false ? (
        <div className="flex">
          <div>
            <img src={iconUser} alt="iconUser"></img>
            moderateur.nom
          </div>
          <div>moderateur.mail</div>
          <div>
            <button onClick={() => supprimer()}>Supprimer</button>
            <button onClick={() => modifier()}>Modifier</button>
          </div>
        </div>
      ) : (
        clicked ===
        true(
          <div>
            <div className="flex">
              <div>
                <img src={iconUser} alt="iconUser"></img>
                moderateur.nom
              </div>
              <div>
                <img src={iconEmail} alt="iconEmail"></img>
                moderateur.mail
              </div>
              <div>
                <button onClick={() => supprimer()}>Supprimer</button>
                <button onClick={() => modifier()}>Modifier</button>
              </div>
            </div>
            <div>
              <img src={iconMdp} alt="iconMdp"></img>
              moderateur.mdp
            </div>
          </div>
        )
      )}
    </div>
  );
}

export default Moderateur;
