// FavoritesList.js
import React, { useEffect, useState } from "react";
import axios from "axios";

const FavoritesList = ({ userId }) => {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    // Fetch user favorites based on userId
    axios
      .get(`http://localhost:8000/user-favorite-articles/?user=${userId}`)
      .then((response) => {
        setFavorites(response.data);
      })
      .catch((error) => {
        console.error("Error fetching user favorites:", error);
      });
  }, [userId]);

  return (
    <div>
      
      <ul>
        {favorites.map((favorite) => (
          <li key={favorite.id}>{favorite.article.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default FavoritesList;
