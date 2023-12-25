import React from "react";

const FavoriePage = () => {
    return(
        <div className="h-full w-screen flex-col  items-center flex font-Futura">
        {/* Background Image */}
        <div
          className="relative w-full justify-center flex flex-col items-center h-[57vh] bg-cover bg-center relative"
          style={{
            backgroundImage: 'url(../../../images/bgimg1.svg)',
          }}
        >
          {/* Overlay Pseudo-element */}
        
  
          {/* Content for the top half */}
          <div className="text-white text-[3vw] z-20 font-Futura-bold mb-[7vh]">
    <p>Découvrez l'excellence</p>
    <p>scientifique en un clic</p>
  </div>
  </div>
  </div>
  
    );
    
  };


export default FavoriePage;