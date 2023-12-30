// FavorisIcon.js
import React, { useState } from "react";
import axios from "axios";
import { BsBookmarks, BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = ({ articleId, onAddToFavorites }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = () => {
    axios
      .post("http://localhost:8000/favoris/", {
        article: articleId,
      })
      .then((response) => {
        setFavoris(true);
        // Trigger the parent component callback to update the list of favorited articles
        onAddToFavorites(articleId);
      })
      .catch((error) => {
        console.error("Error saving favorite article:", error);
      });
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
