import { useState } from "react";
import React from 'react';
import axios from "axios";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";



const FavorisIcon = ({ articleId, user_id }) => {
 
  const [favoris, setFavoris] = useState(false);
  const style = "size-10 text-yellow";

 const addToFavorites = async () => {
   
 };

  return (
    <div>
      {favoris ? (
        <BsBookmarksFill className={style} />
      ) : (
        <BsBookmarks className={style} onClick={addToFavorites} />
      )}
    </div>
  );
};

export default FavorisIcon;
