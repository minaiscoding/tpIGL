// AllArticles.js
import React, { useState, useEffect } from "react";
import Displayer from "../components/Displayer";

/**
 * Functional component for the All articles page.
 *
 * @returns {JSX.Element} - Rendered component.
 */
const FavoriteArticles = () => {
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    console.log("useEffect triggered");

    // Fetch data from the Django API
    fetch("http://localhost:8000/api/userFavoriteArticles/") // Update the URL as needed
      .then((response) => response.json())
      .then((data) => {
        console.log("API Response:", data);
        setSearchResults(data);
      })
      .catch((error) => {
        console.error("Error fetching articles:", error);
      });
  }, []); // Empty dependency array means this effect runs once on mount

  return (
    <div
      className="h-full w-screen min-h-screen font-Futura bg-cover bg-center p-10"
      style={{ backgroundImage: "url(../../../images/bgimg2.svg)" }}
    >
      <div className="mt-8">
        <Displayer results={searchResults} />
      </div>
    </div>
  );
};

export default AllArticles;
