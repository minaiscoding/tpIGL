// FavorisIcon.js

import { useState } from "react";
import axios from "axios";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";


const FavorisIcon = ({ articleId}) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/saveFavorite/",
        {
          articleId: articleId,
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      if (response.status === 200) {
        setFavoris(true);
      }
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
