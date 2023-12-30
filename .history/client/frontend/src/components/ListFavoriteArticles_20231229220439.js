import React, { useState, useEffect } from "react";
import axios from "axios";

const ListFavoriteArticles = () => {
   const [favorisList, setFavorisList] = useState([]);

 useEffect(() => {
   // Fetch the list of favoris from the backend
   axios
     .get("http://localhost:8000/favoris-list/")
     .then((response) => {
       setFavorisList(response.data);
     })
     .catch((error) => {
       console.error("Error fetching favoris list:", error);
     });
 }, []);

  return (
    <div>
      {favorisList.map((favoris) => (
        <div
          key={favoris.id}
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
