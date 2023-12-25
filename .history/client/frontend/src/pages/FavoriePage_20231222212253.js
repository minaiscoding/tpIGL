import React from "react";

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
             <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[7vh]">
  <p>Mes articles préfér</p>
</div>
  </div>
  
  </div>
  
    );
    
  };


export default FavoriePage;