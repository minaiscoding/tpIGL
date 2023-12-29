import React from "react";
import { useState, useEffect } from "react";
import Moderateurs from "../components/Moderateurs";
import iconUser from "../assets/user.png";
import iconMdp from "../assets/iconMdp.png";
import iconEmail from "../assets/iconEmail.png";

const ListModerateurs = () => {
  const [moderateurs, setModerateurs] = useState([]);
  const [ajouté, setAjouté] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const ajouter = () => {
    //integration part
    setAjouté(false)
  };
  let moderateur = {
    NomUtilisateur:" yasmine",
    Email:"ly-choukrane@esi.dz",
    MotDePasse:"azerty",
    role: "moderateur"
  };
  
  useEffect(()=>{setModerateurs([moderateur])},[])

  // useEffect(() => {
  //   console.log("fetching les modérateurs");
  //   fetch(`http://localhost:8000/api/moderateurs`)
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("API Response:", data);
  //       const resultsArray = Object.keys(data).map((key) => data[key]);
  //       setModerateurs(resultsArray);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching les modérateurs:", error);
  //     });
  // }, []);
  return (
    //background
    <div
      className={`relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative ${
        ajouté && "blur-sm"
      }`}
      style={{
        backgroundImage: "url(../../../images/background.svg)",
      }}
    >
      {
        //titre
      }
      <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
        La liste des modérateurs
      </div>
      {
        //liste des modérateurs
      }
      <div>
        <Moderateurs moderateurs={moderateurs} />
      </div>
      {
        //boutton ajouter
      }
      <div>
        <button
          className="place-self-center  bg-gray-800 rounded-md font-Futura text-white w-[10vw] h-[5vh] text-xl text-center "
          onClick={() => setAjouté(true)}
        >
          + Ajouter
        </button>
      </div>
      {
        //formulaire d'ajout
      }
      <div
        className={` blur-none bg-white absolute rounded-xl border-3 border-gray-800 w-[30vw] h-[30vh] p-[1vw] items-center justify-center ${
          !ajouté && "hidden"
        }`}
      >
        <p className="font-Futura font-light text-5xl m-[0vw] flex flex-col items-center justify-center ">
          Ajouter un modérateur
        </p>
        <div className="flex flex-row px-[1vw] w-full h-[25vh]">
          {
            //inputs
          }
          <div className=" p-[0.8vw] my-[1vw] w-2/4  items-center">
            <div className="flex flex-row mb-[2vh]">
              <img className=" " src={iconUser} alt="iconUser"></img>
              <input
                type="text"
                className=" w-[13vw] h-[4vh] p-[0.5vw] text-xl ml-[0.6vw]"
                placeholder="Nom du modérateur"
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-row mb-[2vh]">
              <img
                className="  h-[3vh] mr-[0.5vw]    "
                src={iconEmail}
                alt="iconEmail"
              ></img>
              <input
                type="email"
                className="w-[13vw] h-[4vh] p-[0.5vw] text-lg"
                placeholder="Email du modérateur"
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="flex flex-row mb-[0.8vh]">
              <img
                className="mr-[0.5vw] pb-[6vh]"
                src={iconMdp}
                alt="iconMdp"
              ></img>
              <input
                type="text"
                className=" w-[13vw] h-[4vh] p-[0.5vw] text-lg"
                placeholder="Mot de passe"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          {
            //btn ajouter
          }
          <div className="flex flex-row justify-center items-center h-full w-2/4">
            <button
              className="place-self-center  bg-gray-800 rounded-md font-Futura text-white w-[10vw] h-[5vh] text-xl  "
              onClick={() => ajouter()}
            >
              Ajouter
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ListModerateurs;
