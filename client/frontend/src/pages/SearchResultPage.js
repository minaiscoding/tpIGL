import React, { useState, useEffect } from "react";
import Navbar from "../components/NavBar"; // Import your Navbar component
import Displayer from "../components/Displayer";

const SearchResultPage = () => {
  const getParameterByName = (name, url) => {
    if (!url) url = window.location.href;
    name = name.replace(/[[\]]/g, "\\$&");
    const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
      results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
  };

  // Get the value of the 'q' parameter from the URL
  const qValue = getParameterByName("q");

  const [searchQuery, setSearchQuery] = useState(qValue);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    console.log("useEffect triggered");

    // Fetch search results when the component mounts or when searchQuery changes
    if (searchQuery.trim() !== "") {
      // Fetch search results from your Django API
      console.log("Searching for:", searchQuery);
      fetch(
        `http://localhost:8000/api/search/?q=${encodeURIComponent(searchQuery)}`
      )
        .then((response) => response.json())
        .then((data) => {
          console.log("API Response:", data);
          // Convert the object into an array
          const resultsArray = Object.keys(data).map((key) => data[key]);
          setSearchResults(resultsArray);
        })
        .catch((error) => {
          console.error("Error fetching search results:", error);
        });
    } else {
      setSearchResults([]); // Clear search results if the query is empty
    }
  }, [searchQuery]);

  const handleSearch = () => {
    // Perform the search logic here
    setSearchResults([]); // Clear previous search results

    // For demonstration purposes, let's assume you're ready to navigate to the search results page
    // Replace this with your actual search logic and data fetching
    setSearchResults([
      { id: 1, title: "Result 1", content: "Lorem ipsum 1" },
      { id: 2, title: "Result 2", content: "Lorem ipsum 2" },
      // Add more results as needed
    ]);
  };

  return (
    <div
      className="h-full w-screen min-h-screen font-Futura bg-cover bg-center flex flex-col"
      style={{ backgroundImage: "url(../../../images/bgimg2.svg)" }}
    >
     
      <div className="container mx-auto mt-[8vh]  bg-opacity-80 rounded-lg md:px-[10vw] px-[5vw] md:w-80% w-100%">
        <div className="flex flex-col md:flex-row items-start  space-x-4">
          {/* Search Bar */}
          <div className="flex items-center border border-black rounded-md p-0 bg-gray-800 md:w-auto w-[100%]">
            <input
              type="text"
              placeholder="Rechercher un article"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="rounded-l-md px-4 py-2 bg-white w-[100%] md:w-[30vw] focus:outline-none"
            />
            <button
              onClick={handleSearch}
              className="bg-gray-800 text-white px-4 py-2 rounded-r-md hover:opacity-100"
            >
              Search
            </button>
          </div>

          {/* Date Filters */}
          <div className="flex flex-row items-center space-x-4 md:ml-4 mt-6 md:mt-0 max-w-[90%]">
            <label>Du:</label>
            <input
              type="date"
              className="border border-gray-300 rounded-md px-4 py-2"
            />

            <label>A:</label>
            <input
              type="date"
              className="border border-gray-300 rounded-md px-4 py-2"
            />
          </div>
        </div>

        {/* Filters Section */}
        <div className="mt-8 flex items-center space-x-4">
          {/* Radio Buttons for Filters */}
          <div className="flex items-center space-x-4">
            <label className="flex items-center font-bold">
              <input
                type="radio"
                name="filterType"
                value="option1"
                className="mr-2 h-5 w-5 border-gray-300 border rounded-full"
              />
              <span className="ml-1">Mot Clé</span>
            </label>

            <label className="flex items-center font-bold">
              <input
                type="radio"
                name="filterType"
                value="option2"
                className="mr-2 h-5 w-5 border-gray-300 border rounded-full"
              />
              <span className="ml-1">Auteur</span>
            </label>

            <label className="flex items-center font-bold">
              <input
                type="radio"
                name="filterType"
                value="option2"
                className="mr-2 h-5 w-5 border-gray-300 border rounded-full"
              />
              <span className="ml-1">Titre</span>
            </label>
          </div>
        </div>

        {/* Display Search Results Here */}
        <div className="mt-8">
          <Displayer results={searchResults} />
        </div>
      </div>
    </div>
  );
};

export default SearchResultPage;
