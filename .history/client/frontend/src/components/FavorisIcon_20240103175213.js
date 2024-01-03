// FavorisIcon.js

import { useState } from "react";
import axios from "axios";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";
import { useSelector } from "react-redux";

const FavorisIcon = ({ articleId, user_id }) => {
  const authToken = useSelector((state) => state.auth.token);
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/saveFavorite/",
        {
          articleId: articleId,
          userId: user_id,
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
