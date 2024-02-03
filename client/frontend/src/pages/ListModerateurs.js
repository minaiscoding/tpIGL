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
  useEffect(() => {
    rafraichirModerateur();
  }, []);
  const ajouter = () => {
    let moderateur = {
      NomUtilisateur: username,
      Email: email,
      MotDePasse: password,
      Role: "moderator",
    };

    fetch("http://localhost:8000/api/moderateurs/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(moderateur),
    })
      .then(() => {
        setUsername("");
        setEmail("");
        setPassword("");
        setAjouté(false);
        rafraichirModerateur();
      })
      .catch((error) => {
        console.error("Error adding moderator:", error);
      });
  };
  return (
    //////background
    <div
      className={` w-full justify-center flex flex-col items-center h-screen bg-cover bg-center overflow-y-scroll py-8
      
      `}
      style={{
        backgroundImage: "url(../../../images/background.svg)",
      }}
    >
      {
        //titre
      }
      <div
        className={`text-black text-[5vh] z-20 font-Futura-bold mb-8  ${
          ajouté && "blur-sm brightness-75	"
        }`}
      >
        La liste des modérateurs
      </div>
      {
        //liste des modérateurs
      }
      <div className={`sm:w-[80vw] ${ajouté && "blur-sm brightness-75	"}`}>
        <button
          className="place-self-center  bg-gray-800 rounded-rd font-Futura mt-[0] text-white w-[10vw] h-[5vh] text-xl text-center sm:block w-[25vw] ml-[3vw] md:hidden "
          onClick={() => setAjouté(true)}
        >
          + Ajouter
        </button>
      </div>
      <div className={`${ajouté && "blur-sm brightness-75	"}`}>
        <Moderateurs
          moderateurs={moderateurs}
          setModerateurs={setModerateurs}
        />
      </div>
      {
        //boutton ajouter
      }
      <div>
        <button
          className={`place-self-center  bg-gray-800 rounded-rd font-Futura text-white w-[13vw] h-[7vh] text-xl text-center s:hidden md:block ${
            ajouté && "blur-sm brightness-75	"
          }`}
          onClick={() => setAjouté(true)}
        >
          + Ajouter
        </button>
      </div>
      {
        //formulaire d'ajout
      }
      <div
        className={` blur-none bg-white absolute border-2 border-dashed border-gray-800 rounded-rd w-[35vw] h-[37vh] p-[1vw] items-center justify-center s:w-[43vw] ${
          !ajouté && "hidden"
        } ${ajouté && "blur-none brightness-100	"}`}
      >
        <p className="font-Futura font-light text-3xl m-[0vw] flex flex-col items-center justify-center s:text-2xl ">
          Ajouter un modérateur
        </p>
        <div className="flex flex-row px-[1vw] w-full h-[25vh]">
          {
            //inputs
          }
          <div className=" p-[0.8vw] my-[1vw] w-2/4  items-center">
            <div className="flex flex-row mb-[2vh]">
              <img
                className="mr-[1vw] w-[5vw] h-[5.5vh] mp-[1vh] "
                src={iconUser}
                alt="iconUser"
              ></img>
              <input
                type="text"
                className=" w-[13vw] h-[4vh] p-[0.5vw] text- ml-[0.3vw] mt-[0.5vh] s:text-sm s:w-[20vw]"
                placeholder="Nom du modérateur"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-row mb-[2vh]">
              <img
                className="mr-[1vw] w-[4vw] h-[4vh] mt-[1vh] "
                src={iconEmail}
                alt="iconEmail"
              ></img>
              <input
                type="email"
                className="w-[13vw] h-[4vh] p-[0.5vw] text mt-[1vh] s:text-sm s:w-[23vw]"
                placeholder="Email du modérateur"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="flex flex-row mb-[0.8vh]">
              <img
                className="mr-[1vw] w-[5.5vw] h-[6vh] mt-[0.5vh] "
                src={iconMdp}
                alt="iconMdp"
              ></img>
              <input
                type="text"
                className=" w-[13vw] h-[4vh] p-[0.5vw] text mt-[2vh] s:text-sm s:w-[20vw]"
                placeholder="Mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          {
            //btn ajouter
          }
          <div className="flex flex-row justify-center items-center h-full w-2/4">
            <button
              className="place-self-center  bg-gray-800 rounded-rd font-Futura text-white w-[10vw] h-[7vh] text-xl s:text-xs s:mr-[vw] "
              onClick={() => {
                ajouter();
              }}
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