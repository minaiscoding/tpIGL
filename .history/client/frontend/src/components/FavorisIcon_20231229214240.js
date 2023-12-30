import { useState } from "react";
import React from 'react';
import axios from "axios";
import { BsBookmarks } from "react-icons/bs";


const FavorisIcon = () => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = () => {
    
  };

  

  return (
    <div>
        {favoris ? (
        <BsBookmarks className={style} onClick={addToFavorites} /> ): null}
    </div>
  );
};

export default FavorisIcon;
