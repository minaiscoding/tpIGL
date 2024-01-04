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
    <div
      className="h-full w-screen min-h-screen font-Futura bg-cover bg-center p-10"
      style={{ backgroundImage: "url(../../../images/bgimg2.svg)" }}
    >
      <div className="text-black text-[3vw] z-50 font-Futura-bold mb-[10vh]">
        <p>Mes articles favoris</p>
      </div>
      <div className="mt-8">
        <Displayer results={searchResults} />
      </div>
    </div>
  );
};

export default FavoriteArticles;
