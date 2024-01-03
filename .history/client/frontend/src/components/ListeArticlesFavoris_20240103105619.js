import React, { useState, useEffect } from "react";
import axios from "axios";

const ListFavoriteArticles = () => {
  const [favoriteArticles, setFavoriteArticles] = useState([]);

  useEffect(() => {
    // Fetch favorite articles from the backend
    axios
      .get("http://localhost:8000/favori/")
      .then((response) => {
        setFavoriteArticles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching favorite articles:", error);
      });
  }, []);

  return (
    <div>
      <h2>Favorite Articles</h2>
      <ul>
        {favoriteArticles.map((article) => (
          <li key={article.id}>{article.article.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default ListFavoriteArticles;
