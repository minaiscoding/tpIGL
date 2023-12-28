import React from "react";
import { useState } from "react";
import iconUser from "../assets/iconUser.png";
import iconMdp from "../assets/iconMdp.png";
import iconEmail from "../assets/iconEmail.png";
function Moderateur({moderateur}) {
  const [clicked, setClicked] = useState(false);
  const [modifié, setModifié] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
  const supprimer = (nom) => {
    //integration part
  };
  const modifier = (nom) => {
    setModifié(true);
    setClicked(true);
  };
  const save=()=>{
    //integration part
    setModifié(false);
  }
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
            <button onClick={() => supprimer(moderateur.nom)}>Supprimer</button>
            <button onClick={() => modifier(moderateur.nom)}>Modifier</button>
          </div>
        </div>
      ) : (
        clicked ===
        true(
          modifié === false ? (
            <div>
              <div>
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
          ) : (
            modifié ===
              true(
                <div>
                  <div>
                    <div>
                      <img src={iconUser} alt="iconUser"></img>
                      <input
                        type="text"
                        value={moderateur.nom}
                        onChange={(e) => setUsername(e.target.value)}
                      />
                    </div>
                    <div>
                      <img src={iconEmail} alt="iconEmail"></img>
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
                    <img src={iconMdp} alt="iconMdp"></img>
                    <input
                      type="text"
                      value={moderateur.mdp}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                </div>
              )
          )
        )
      )}
    </div>
  );
}

export default Moderateur;

// il faut creer le formulaire d'ajout position absolue hidden
// il faut appliquer les styles
//il faut se mettre au back
//tu dois terminer aujourd'hui
