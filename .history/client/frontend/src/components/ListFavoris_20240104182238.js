// AllArticles.js
import React, { useState, useEffect } from "react";
import Displayer from "../components/Displayer";

/**
 * Functional component for the Favorite articles page.
 *
 * @returns {JSX.Element} - Rendered component.
 */

const FavoriteArticles = () => {
  const [searchResults, setSearchResults] = useState([]);

  const userId = localStorage.getItem("id");

  useEffect(() => {
    console.log("useEffect triggered");

    // Fetch data from the Django API with the user ID included
    fetch(`http://localhost:8000/api/favoris/${userId}/`) // Update the URL as needed
      .then((response) => response.json())
      .then((data) => {
        console.log("API Response:", data);
        setSearchResults(data);
      })
      .catch((error) => {
        console.error("Error fetching articles:", error);
      });
  }, [userId]); // Include userId in the dependency array to re-run the effect when userId changes

  return (
    <div>
      {sortedResults.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border-2 rounded-rd border-black rounded-md p-5 mb-5 result-container ml-10 mr-10 transition duration-300 ease-in-out hover:border-4"
          style={{ display: "flex", flexDirection: "column" }}
        >
          
          <h1 className="pl-5 pr-5 text-3xl font-bold">{result.Titre}</h1>
          <p className="text-gray-800 text-opacity-75 italic mb-2 mt-2 pl-5 pr-5">
            {result.id}
          </p>
          <p className="text-gray-800 text-opacity-75 italic mb-2 mt-2 pl-5 pr-5">
            {result.auteurs}
          </p>
          <p className="text-gray-800 text-opacity-75 italic mb-1 mt-1 pl-5 pr-5">
            {result.date}
          </p>
          <p className="pl-5 pr-5 mb-2 mt-2">{result.Resume}</p>
          <a
            href={result.URL_Pdf}
            className="pl-5 pr-5 mb-2 mt-2 font-bold text-yellow hover:text-purple-800 no-underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            Voir l'article complet en PDF
          </a>

          {/* 
            Additional content can be added here.
            For example, you can include more information from the 'result' object.
          */}
        </div>
      ))}
    </div>
  );
};

export default FavoriteArticles;
