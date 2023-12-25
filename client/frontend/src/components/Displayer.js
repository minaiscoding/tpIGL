// Displayer.js
import React from "react";

const Displayer = ({ results }) => {
  return (
    <div>
      {results.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border border-black rounded-md p-4 mb-4"
        >
          <h2>{result.Titre}</h2>
          <p>{result.Resume}</p>
          {/* Add more content as needed */}
        </div>
      ))}
    </div>
  );
};

export default Displayer;
