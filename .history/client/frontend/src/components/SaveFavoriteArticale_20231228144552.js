import React, { useState, useEffect } from "react";
import axios from "axios";

const SaveFavoriteArticle = ({ articleId }) => {
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    // Send a POST request to save the article as a favorite
    
  };

  return (
    <div>
      {!isSaved ? (
        <button onClick={handleSave}>Save as Favorite</button>
      ) : (
        <p>Article saved as favorite!</p>
      )}
    </div>
  );
};

export default SaveFavoriteArticle;
