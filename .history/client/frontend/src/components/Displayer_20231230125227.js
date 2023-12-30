// Displayer.js
import React, { useState } from "react";
import FavorisIcon from "./FavorisIcon";

const Displayer = ({ results }) => {
  const [favoritedArticles, setFavoritedArticles] = useState([]);

  const handleAddToFavorites = (articleId) => {
    setFavoritedArticles([...favoritedArticles, articleId]);
  };

  return (
    <div>
      {results.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border border-black rounded-md p-4 mb-4 result-container"
          style={{ display: "flex", flexDirection: "column" }}
        >
          <div style={{ alignSelf: "flex-end" }}>
            <FavorisIcon
              articleId={result.id}
              onAddToFavorites={handleAddToFavorites}
            />
          </div>
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

export default Displayer;
