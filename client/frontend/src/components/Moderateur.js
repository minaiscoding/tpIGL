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
    console.log(modifieModerateur)
    console.log(password)
    console.log(moderateur.MotDePasse)

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
              onClick={() => supprimer(moderateur.id)}
            >
              Supprimer
            </button>
            <button
              className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
              onClick={() => modifier()}
            >
              Modifier
            </button>
          </div>
        </div>
      ) : !modifié ? (
        <div className=" bg-white w-[80vw] h-[18vh] border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between">
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
                onClick={() => supprimer(moderateur.id)}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => modifier()}
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
        <div className=" bg-white w-[80vw] h-[18vh] text-gray-800 border-2 rounded-rd	 p-[2vw] m-[3vh] flex  flex-col justify-items-center justify-between">
          <div className="flex  flex-row justify-items-center justify-between">
            <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-center ">
              <img
                src={iconUser}
                alt="iconUser"
                className="mr-[1vw] mt-[0vh] w-[2vw] h-[5vh] pb-[1vh] w-full h-full"
              />
              <input
                type="text"
                placeholder={moderateur.NomUtilisateur}
                value={username || moderateur.NomUtilisateur}
                className="p-[0.5vw] pt-[0] mb-[0.3vh] "
                onChange={(e) => 
                  setUsername(e.target.value)}
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
                placeholder={moderateur.Email}
                value={email || moderateur.Email}
                className="p-[0.5vw] pt-[0] mb-[0.3vh] "
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <button
                className="bg-gray-800 rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => supprimer(moderateur.id)}
              >
                Supprimer
              </button>
              <button
                className="bg-yellow rounded-rd font-Futura text-white w-[8vw] h-[5vh] text-2xl text-center justify-self-center mr-[1vw] "
                onClick={() => save(moderateur.id)}
              >
                Save
              </button>
            </div>
          </div>
          <div className="flex flex-row  text-3xl	font-normal	justify-items-center justify-start py-[0.5vw]">
            <img
              src={iconMdp}
              alt="iconMdp"
              className="mr-[1vw] mt-[0.5vh] w-[2vw] h-[5vh] pb-[1vh] "
            />
            <input
              type="text"
              placeholder={moderateur.MotDePasse}
              value={ password || moderateur.MotDePasse}
              className="p-[0.5vw]  "
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Moderateur;
