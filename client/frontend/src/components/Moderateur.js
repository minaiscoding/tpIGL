import React from "react";
import { useState } from "react";
import iconUser from "../assets/user.png";
import iconMdp from "../assets/iconMdp.png";
import iconEmail from "../assets/iconEmail.png";
import axios from "axios";

function Moderateur({ moderateur, setModerateurs }) {
  const [clicked, setClicked] = useState(false);
  const [modifié, setModifié] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const rafraichirModerateur = () => {
    console.log("fetching les modérateurs");
    fetch(`http://localhost:8000/api/moderateurs`)
      .then((response) => response.json())
      .then((data) => {
        console.log("API Response:", data);
        const resultsArray = Object.keys(data).map((key) => data[key]);
        setModerateurs(resultsArray);
      })
      .catch((error) => {
        console.error("Error fetching les modérateurs:", error);
      });
  };
  const supprimer = (id) => {
    fetch(`http://localhost:8000/api/moderateurs/delete/${id}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then(() => {
        setClicked(false);
        rafraichirModerateur();
      })
      .catch((error) => {
        console.error("Error deleting moderator:", error);
      });
  };

  const modifier = (nom) => {
    setModifié(true);
    setClicked(true);
  };

  const save = (id) => {
    // Construire l'objet modifié avec les nouvelles valeurs

    let modifieModerateur = {
      NomUtilisateur: username || moderateur.NomUtilisateur,
      Email: email || moderateur.Email,
      MotDePasse: password || moderateur.MotDePasse,
      Role: "moderator",
    };
    console.log(modifieModerateur);
    console.log(password);
    console.log(moderateur.MotDePasse);

    // Envoyer une requête pour mettre à jour le modérateur avec le nom spécifié
    axios
      .post(
        `http://localhost:8000/api/moderateurs/update/${id}`,
        modifieModerateur
      )
      .then(() => {
        // Rafraîchir la liste des modérateurs après la mise à jour
        rafraichirModerateur();
        setModifié(false); // Réinitialiser l'état modifié
        setClicked(false); // Réinitialiser l'état clicked
      })
      .catch((error) => {
        console.error("Erreur lors de la mise à jour du modérateur:", error);
      });
  };

  return (
    <div>
      {!clicked ? (
        <div
          className=" rounded-rd  bg-white w-[80vw] h-[12vh] border-2  p-[1vw] flex flex-row justify-between m-[1.5vh]  justify-items-center	font-Futura s:pt-[3vh]
	 	"
          onClick={() => setClicked(!clicked)}
        >
          <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-lg	">
            <img
              className="mr-[1vw] w-[3vw] h-[6vh] pb-[0.vh] s:h-[5vh] s:mt-[0.5vh]"
              src={iconUser}
              alt="iconUser"
            />
            {moderateur.NomUtilisateur}
          </div>
          <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-lg">
            {moderateur.Email}
          </div>
          <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center pt-[0vh] s:text-sm">
            <button
              className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs s:w-[9vw]"
              onClick={() => supprimer(moderateur.id)}
            >
              Supprimer
            </button>
            <button
              className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs"
              onClick={() => modifier()}
            >
              Modifier
            </button>
          </div>
        </div>
      ) : !modifié ? (
        <div className=" bg-white w-[80vw] h-[22vh] border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between">
          <div className="flex  flex-row justify-items-center justify-between">
            <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-base ">
              <img
                src={iconUser}
                alt="iconUser"
                className="mr-[1vw] w-[3vw] h-[5.5vh] mt-[1vh] s:h-[4vh]"
              />
              {moderateur.NomUtilisateur}
            </div>
            <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-base">
              <img
                src={iconEmail}
                alt="iconEmail"
                className="mr-[1vw] w-[2vw] h-[5vh] mt-[1vh] s:h-[4vh]"
              />
              {moderateur.Email}
            </div>
            <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center pt-[0vh]">
              <button
                className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs s:w-[9vw] "
                onClick={() => supprimer(moderateur.id)}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs  "
                onClick={() => modifier()}
              >
                Modifier
              </button>
            </div>{" "}
          </div>
          <div className="flex flex-row mt[0.5vh] text-xl	font-normal	justify-items-center justify-start py-[1vw] w-[10vw] s:text-sm ">
            <img
              src={iconMdp}
              alt="iconMdp"
              className="mr-[1vw] ml-[0vw] w-[3vw] h-[6vh] mt-[0.5vh]"
            />
            <div className="pt-[0.5vh] w-[80vw] pr-[1vw] s:mt-[1vh]  ">
              {moderateur.MotDePasse}
            </div>
          </div>
        </div>
      ) : (
        <div className=" bg-white w-[80vw] h-[22vh] border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between">
          <div className="flex  flex-row justify-items-center justify-between">
            <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-base">
              <img
                src={iconUser}
                alt="iconUser"
                className="mr-[1vw] w-[3vw] h-[5.5vh] mt-[1vh]"
              />
              <input
                type="text"
                placeholder={moderateur.NomUtilisateur}
                value={username || moderateur.NomUtilisateur}
                className="p-[0.5vw] pt-[0] mb-[0.3vh] w-[14vw] s:w-[16vw] "
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-row  text-2xl	font-normal	justify-items-center justify-center s:text-base ">
              <img
                src={iconEmail}
                alt="iconEmail"
                className="mr-[1vw] w-[2vw] h-[5vh] mt-[1vh] s:h-[4vh] s:pt-[0.5vh]"
              />
              <input
                type="email"
                placeholder={moderateur.Email}
                value={email || moderateur.Email}
                className="p-[0.5vw] pt-[0] mb-[0.3vh] w-[25vw]  "
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <button
                className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs s:w-[9vw]"
                onClick={() => supprimer(moderateur.id)}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[6vh] text-xl text-center justify-self-center p-[2px] mr-[1vw] mt-[0vw] s:text-xs"
                onClick={() => save(moderateur.id)}
              >
                Save
              </button>
            </div>
          </div>
          <div className="flex flex-row  text-xl	font-normal	justify-items-center justify-start py-[0.5vw] s:text-sm">
            <img
              src={iconMdp}
              alt="iconMdp"
              className="mr-[1vw] ml-[0vw] w-[3vw] h-[6vh] mt-[0.5vh]"
            />
            <input
              type="text"
              placeholder={moderateur.MotDePasse}
              value={password || moderateur.MotDePasse}
              className="p-[0.5vw] w-[100%] "
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Moderateur;