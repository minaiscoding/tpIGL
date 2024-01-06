// FavorisIcon.js

import { useState } from "react";
import axios from "axios";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = ({ articleId, user_id }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = async () => {
    try {
      
      const await axios.post(
        "http://localhost:8000/api/saveFavorite/",
        {
          articleId: articleId,
          userId: user_id,
        }
      );
     console.log("API response:", response);
      setFavoris(true);
    } catch (error) {
      console.error("Error saving favorite article:", error);
    }
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
