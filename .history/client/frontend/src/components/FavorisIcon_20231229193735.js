import { useState } from "react";
import React from 'react';
import axios from "axios";
import { BsBookmarks } from "react-icons/bs";


const FavorisIcon = ({ articleId }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  

  

  return (
    <div>
        {favoris ? (
        <BsBookmarks className={style} onClick={addToFavorites} /> ): null}
    </div>
  );
};

export default FavorisIcon;
