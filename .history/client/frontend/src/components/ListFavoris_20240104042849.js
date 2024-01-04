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
    fetch(`http://localhost:8000/api/userFavoriteArticles/${userId}/`) // Update the URL as needed
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
    <div className="mt-8">
      <Displayer results={searchResults} />
    </div>
  );
};

export default FavoriteArticles;
