import React, { useState, useEffect } from "react";
import axios from "axios";

const ListFavoriteArticles = () => {
  const [favoriteArticles, setFavoriteArticles] = useState([]);

  useEffect(() => {
    // Fetch favorite articles from the backend
    axios
      .get("http://localhost:8000/mesFavorite-articles/")
      .then((response) => {
        setFavoriteArticles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching favorite articles:", error);
      });
  }, []);

  return (
    <div>
      {favoriteArticles.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border border-black rounded-md p-4 mb-4"
        >
          <h2>{result.Titre}</h2>
          <p>{result.Resume}</p>
          {/* 
            Additional content can be added here.
            For example, you can include more information from the 'result' object.
          */}
        </div>
      ))}
    </div>
  );
};

export default ListFavoriteArticles;
