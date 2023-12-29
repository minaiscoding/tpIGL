import React from "react";
import { useState } from "react";
import iconUser from "../assets/iconUser.png";
import iconMdp from "../assets/iconMdp.png";
import iconEmail from "../assets/iconEmail.png";

function Moderateur({ moderateur }) {
  const [clicked, setClicked] = useState(false);
  const [modifié, setModifié] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const supprimer = (nom) => {
    // integration part
  };

  const modifier = (nom) => {
    setModifié(true);
    setClicked(true);
  };

  const save = () => {
    // integration part
    setModifié(false);
  };

  return (
    <div onClick={() => setClicked(!clicked)}>
      {!clicked ? (
        <div className="flex">
          <div>
            <img src={iconUser} alt="iconUser" />
            {moderateur.NomUtilisateur}
          </div>
          <div>{moderateur.Email}</div>
          <div>
            <button onClick={() => supprimer(moderateur.nom)}>Supprimer</button>
            <button onClick={() => modifier(moderateur.nom)}>Modifier</button>
          </div>
        </div>
      ) : !modifié ? (
        <div>
          <div>
            <div>
              <img src={iconUser} alt="iconUser" />
              {moderateur.NomUtilisateur}
            </div>
            <div>
              <img src={iconEmail} alt="iconEmail" />
              {moderateur.mail}
            </div>
            <div>
              <button onClick={() => supprimer()}>Supprimer</button>
              <button onClick={() => modifier()}>Modifier</button>
            </div>
          </div>
          <div>
            <img src={iconMdp} alt="iconMdp" />
            {moderateur.MotDePasse}
          </div>
        </div>
      ) : (
        <div>
          <div>
            <div>
              <img src={iconUser} alt="iconUser" />
              <input
                type="text"
                value={moderateur.nom}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <img src={iconEmail} alt="iconEmail" />
              <input
                type="email"
                value={moderateur.mail}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <button onClick={() => supprimer()}>Supprimer</button>
              <button onClick={() => save()}>Save</button>
            </div>
          </div>
          <div>
            <img src={iconMdp} alt="iconMdp" />
            <input
              type="text"
              value={moderateur.mdp}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Moderateur;
