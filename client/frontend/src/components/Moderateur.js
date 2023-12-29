import React from "react";
import { useState } from "react";
import iconUser from "../assets/user.png";
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
    <div>
      {!clicked ? (
        <div
          className="flex bg-white w-[80vw] h-[12vh] border-2 rounded-md p-[2vw] flex flex-row justify-between m-[3vh]  justify-items-center	font-Futura
	 	"
          onClick={() => setClicked(!clicked)}
        >
          <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center ">
            <img
              className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
              src={iconUser}
              alt="iconUser"
            />
            {moderateur.NomUtilisateur}
          </div>
          <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center">
            {moderateur.Email}
          </div>
          <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center pt-[0vh]">
            <button
              className="bg-gray-800 rounded-md font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
              onClick={() => supprimer(moderateur.nom)}
            >
              Supprimer
            </button>
            <button
              className="bg-yellow rounded-md font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
              onClick={() => modifier(moderateur.nom)}
            >
              Modifier
            </button>
          </div>
        </div>
      ) : !modifié ? (
        <div
          className="flex bg-white w-[80vw] h-[12vh] border-2 rounded-md p-[2vw] flex flex-row justify-between m-[3vh]  justify-items-center	font-Futura
	 	"
          onClick={() => setClicked(!clicked)}
        >
          <div>
            <div>
              <img src={iconUser} alt="iconUser" />
              {moderateur.NomUtilisateur}
            </div>
            <div>
              <img src={iconEmail} alt="iconEmail" />
              {moderateur.Email}
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
