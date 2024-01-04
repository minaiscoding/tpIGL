// FavoriteArticlesList.js
import React, { useState, useEffect } from "react";
import axios from "axios";

const FavoriteArticlesList = ({ userId }) => {
  const [favoriteArticles, setFavoriteArticles] = useState([]);

  useEffect(() => {
    // Fetch favorite articles for the specified user from Django backend
    axios
      .get(`http://localhost:8000/api/userFavoriteArticles/${userId}/`)
      .then((response) => {
        setFavoriteArticles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching favorite articles:", error);
      });
  }, [userId]);

  return (
    <div>
      <h2>Your Favorite Articles</h2>
      <ul>
        {favoriteArticles.map((favorite) => (
          <li key={favorite.id}>
            {/* Display information about the favorited article as needed */}
            {favorite.ArticleID.Titre}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FavoriteArticlesList;
