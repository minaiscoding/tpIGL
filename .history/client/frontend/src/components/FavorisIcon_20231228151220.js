import { useState } from "react";
import React from 'react';
import axios from "axios";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = ({ articleId, favoriteArticleId, onDeleted }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = () => {
    axios
      .post("http://localhost:8000/favorite-articles/", {
        article: articleId,
      })
      .then((response) => {
        setFavoris(true);
      })
      .catch((error) => {
        console.error("Error saving favorite article:", error);
      });
  };

  

  return (
    <div>
      favoris ? (
        <BsBookmarks className={style} onClick={addToFavorites} /> )}
    </div>
  );
};

export default FavorisIcon;
