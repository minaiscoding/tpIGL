import React from "react";
import  { useState, useEffect } from "react";
import Moderateurs from "../components/Moderateurs";



const ListModerateurs=()=> {
  const [moderateurs, setModerateurs] = useState([]);
  const [ajouté,setAjouté]=useState(false)

  useEffect(() => {
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
  },[]);
  return (
    <div
      className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative"
      style={{
        backgroundImage: "url(../../../images/background.svg)",
      }}
    >
      <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
        La liste des modérateurs
      </div>
      <div>
       <Moderateurs moderateurs={moderateurs}/>
      </div>
      <div>
        <button  onClick={()=>setAjouté(true)}>Ajouter</button>
      </div>
    </div>
  );
}
export default ListModerateurs;