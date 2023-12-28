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

  const deleteFromFavorites = () => {
    axios
      .delete(`http://localhost:8000/favorite-articles/${favoriteArticleId}/`)
      .then((response) => {
        // Notify the parent component that the article has been deleted
        onDeleted();
      })
      .catch((error) => {
        console.error("Error deleting favorite article:", error);
      });
    setFavoris(false);
  };

  return (
    <div>
      {favoris ? (
        <BsBookmarksFill className={style} onClick={deleteFromFavorites} />
      ) : (
        <BsBookmarks className={style} onClick={addToFavorites} />
      )}
    </div>
  );
};

export default FavorisIcon;
