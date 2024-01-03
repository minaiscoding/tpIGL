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
      const response = await axios.post(
        `/api/AddToFavorite/${user_id}/${articleId}/`,
        {
          user_id: user_id,
          article_id: articleId,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        setFavoris(true);
        // Optionally, you can show a success message or update the UI
      } else {
        // Handle the error
      }
    } catch (error) {
      console.error("Error adding to favorites:", error);
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
