// Displayer.js
import React from "react";
import FavorisIcon from "./FavorisIcon";

/**
 * Functional component to display results.
 *
 * @param {Object} props - React component props.
 * @param {Array} props.results - Array of result objects to be displayed.
 * @returns {JSX.Element} - Rendered component.
 */
const Displayer = ({ results }) => {
 const userId= 4;
  if (results.length === 0) {
    return <p style={{ color: "black" }}>Pas de résultat</p>;
  }

  return (
    <div>
      {results.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border border-black rounded-md p-4 mb-4 result-container"
          style={{ display: "flex", flexDirection: "column" }}
        >
          <div style={{ alignSelf: "flex-end" }}>
            <FavorisIcon user_id={userId} articleId={result.id} />
          </div>
          <h2>{result.Titre}</h2>
          <p>{result.Resume}</p>
          <p>{result.id}</p>
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
