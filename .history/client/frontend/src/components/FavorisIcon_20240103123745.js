// FavorisIcon.js

import { useState, useEffect } from "react";
import axios from "axios";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = ({ articleId }) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

const fetchFavoriteArticles = useMemo(
    () => async () => {
  try {
    // Make an API request to get the user's favorite articles
    const response = await axios.get(`http://localhost:8000/favorite/`);

    // Check if the current article is in the list of favorites
    const isFavorited = response.data.some(
      (favorite) => favorite.article.id === articleId
    );

    // Update the 'favorited' state based on the result
    setFavoris(isFavorited);
  } catch (error) {
    console.error("Error fetching user's favorite articles:", error);
  }
};

    useEffect(() => {
           fetchFavoriteArticles(); 
    }, [fetchFavoriteArticles]);

  const addToFavorites = async () => {
    axios
      .post("http://localhost:8000/favorite/", { article: articleId })
      .then((response) => {
        setFavoris(true);
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
