// Displayer.js
import React from "react";
import FavorisIcon from "./FavorisIcon";
import { Link } from "react-router-dom";
import { useEffect } from "react";


import { Pointer } from "lucide-react";

/**
 * Functional component to display results.
 *
 * @param {Object} props - React component props.
 * @param {Array} props.results - Array of result objects to be displayed.
 * @returns {JSX.Element} - Rendered component.
 */






const Displayer = ({ results }) => {
  // Sort the results by date in descending order
  const sortedResults = [...results].sort((a, b) => new Date(b.date) - new Date(a.date));

  if (sortedResults.length === 0) {
    return <p style={{ color: "black" }}>Pas de résultat</p>;
  }


  return (
    <div>

      {sortedResults.map((result) => (

        <div
          key={result.Titre}
          className="bg-white border-2 rounded-rd border-black rounded-md p-5 mb-5 result-container ml-10 mr-10 transition duration-300 ease-in-out hover:border-4"
          style={{ display: "flex", flexDirection: "column" }}>

          <div style={{ alignSelf: "flex-end" }} className="w-10">

            <FavorisIcon articleID= {}>
          </div>
          <h1 className="pl-5 pr-5 text-3xl font-bold">{result.Titre}</h1>
          <p className="text-gray-800 text-opacity-75 italic mb-2 mt-2 pl-5 pr-5">{result.auteurs}</p>
          <p className="text-gray-800 text-opacity-75 italic mb-1 mt-1 pl-5 pr-5">{result.date}</p>
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
      ))
      }
    </div >
  );
};

export default Displayer;
