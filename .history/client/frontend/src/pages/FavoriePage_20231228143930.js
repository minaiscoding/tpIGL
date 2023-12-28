import React, { useState, useEffect } from "react";
import ListFavoriteArticles from "../components/ListFavoriteArticles";

const FavoriePage = () => {
  const [favoriesResults, setfavoriesResults] = useState([]);

    return (
      <div
        className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative"
        style={{
          backgroundImage: "url(../../../images/background.svg)",
        }}
      >
        <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
          <p>Mes articles favoris</p>
        </div>
        {/* Display Search Results Here */}
        <div className="mt-8">
          <ListFavoriteArticles results={favoriesResults} />
        </div>
        <div>
          <FavorisIcon />
        </div>
      </div>
    );
    
  };


export default FavoriePage;