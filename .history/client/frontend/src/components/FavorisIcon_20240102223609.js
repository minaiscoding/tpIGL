// FavorisIcon.js

import { useState } from "react";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = ({ articleId }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = async () => {
    try {
      const response = await fetch(`/api/favoris/${articleId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${YOUR_ACCESS_TOKEN}`, // Add your authentication token
        },
      });

      if (response.ok) {
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
