import React from "react";
//import DataDisplay from '../components/DataDisplay';

const FavoriePage = () => {
    return(
        <div>
           
        {/* Background Image */}
        <div
          className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative"
          style={{
            backgroundImage: 'url(../../../images/background.svg)',
          }}
        >
             <div className="text-black text-[3vw]  font-Futura-bold mb-[7vh]">
             <p>Mes articles favoris</p>
             </div>
  </div>
  
  </div>
  
    );
    
  };


export default FavoriePage;