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
          className=" rounded-rd  bg-white w-[80vw] h-[12vh] border-2  p-[2vw] flex flex-row justify-between m-[3vh]  justify-items-center	font-Futura
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
              className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
              onClick={() => supprimer(moderateur.nom)}
            >
              Supprimer
            </button>
            <button
              className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
              onClick={() => modifier(moderateur.NomUtilisateu)}
            >
              Modifier
            </button>
          </div>
        </div>
      ) : !modifié ? (
        <div
          className=" bg-white w-[80vw] h-[18vh] border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between"
          onClick={() => setClicked(!clicked)}
        >
          <div className="flex  flex-row justify-items-center justify-between">
            <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center ">
              <img
                src={iconUser}
                alt="iconUser"
                className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
              />
              {moderateur.NomUtilisateur}
            </div>
            <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center">
              <img
                src={iconEmail}
                alt="iconEmail"
                className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
              />
              {moderateur.Email}
            </div>
            <div>
              <button
                className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => supprimer(moderateur.NomUtilisateu)}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => modifier(moderateur.NomUtilisateu)}
              >
                Modifier
              </button>
            </div>
          </div>
          <div className="flex flex-row mt[0.5vh] text-3xl	font-normal	justify-items-center justify-start py-[1vw]">
            <img
              src={iconMdp}
              alt="iconMdp"
              className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
            />
            <div className="pt-[0.5vh]">{moderateur.MotDePasse}</div>
          </div>
        </div>
      ) : (
        <div className=" bg-white w-[80vw] h-[18vh] border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between">
          <div className="flex  flex-row justify-items-center justify-between">
            <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center ">
              <img
                src={iconUser}
                alt="iconUser"
                className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center"
              />
              <input
                type="text"
                value={moderateur.NomUtilisateur}
                className=""
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center">
              <img
                src={iconEmail}
                alt="iconEmail"
                className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
              />
              <input
                type="email"
                value={moderateur.Email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <button
                className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => supprimer()}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => save()}
              >
                Save
              </button>
            </div>
          </div>
          <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-start py-[0.5vw]">
            <img
              src={iconMdp}
              alt="iconMdp"
              className="mr-[1vw] w-[2vw] h-[5vh] pb-[1vh]"
            />
            <input
              type="text"
              value={moderateur.MotDePasse}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Moderateur;
