// Your React component
import React, { useState, useEffect } from "react";
import axios from "axios";

const FavoriteArticlesList = () => {
  const [favoriteArticles, setFavoriteArticles] = useState([]);

  useEffect(() => {
    // Fetch favorite articles from Django backend
    axios
      .get("http://localhost:8000/user-favorite-articles/")
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
