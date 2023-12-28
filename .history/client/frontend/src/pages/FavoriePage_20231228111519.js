import React from "react";
import Displayer from "../components/Displayer";
//import DataDisplay from '../components/DataDisplay';
import FavorisIcon from "../components/FavorisIcon";

const FavoriePage = () => {
    return (
      <div>
        {/* Background Image */}
        <div
          className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative"
          style={{
            backgroundImage: "url(../../../images/background.svg)",
          }}
        >
          <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
            <p>Mes articles favoris</p>
          </div>
          <div>
           Favo
          </div>
        </div>
      </div>
    );
    
  };


export default FavoriePage;