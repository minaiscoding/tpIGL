// FavoriteArticlesList.js
import React, { useState, useEffect } from "react";
import axios from "axios";

const FavoriteArticlesList = () => {
  const [favoriteArticles, setFavoriteArticles] = useState([]);

  useEffect(() => {
    // Make an API request to fetch the user's favorite articles
    axios
      .get("http://localhost:8000/favorite/")
      .then((response) => {
        setFavoriteArticles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching favorite articles:", error);
      });
  }, []);

  return (
    <div>
      <h2>Your Favorite Articles</h2>
      <ul>
        {favoriteArticles.map((favorite) => (
          <li key={favorite.id}>
            {/* Display information about the favorited article as needed */}
            {favorite.article.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FavoriteArticlesList;
