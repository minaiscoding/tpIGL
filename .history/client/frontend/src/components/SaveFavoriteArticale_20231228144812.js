import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SaveFavoriteArticle = ({ articleId }) => {
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    // Send a POST request to save the article as a favorite
    axios.post('http://localhost:8000/favorite-articles/', { article: articleId })
      .then(response => {
        setIsSaved(true);
      })
      .catch(error => {
        console.error('Error saving favorite article:', error);
      });
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
