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
          <div className="absolute inset-0 bg-gradient-to-r from-[#3635CE] to-[#F6B237] opacity-80 z-10"></div>
  
          {/* Content for the top half */}
          <div className="text-white text-[3vw] z-20 font-Futura-bold mb-[7vh]">
    <p>Découvrez l'excellence</p>
    <p>scientifique en un clic</p>
  </div>
  
    );
    
  };


export default FavoriePage;