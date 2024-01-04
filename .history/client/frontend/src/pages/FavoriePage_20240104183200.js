import React from "react";
import ListFavoris from '../components/ListFavoris';


const FavoriePage = () => {
    return (
      <div>
        {/* Background Image */}
        <div
          className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center"
          style={{
            backgroundImage: "url(../../../images/background.svg)",
          }}
        >
          <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
            <p>Mes articles favoris</p>
          </div>
          
        </div>
        
      </div>
    );
    
  };


export default FavoriePage;