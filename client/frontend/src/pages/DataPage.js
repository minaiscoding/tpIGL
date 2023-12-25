// Displayer.js
import React from "react";

const Displayer = ({ results }) => {
  return (
    <div className="bg-white border border-black rounded-md p-4">
      {/* Map through searchResults and display each result */}
      {results.map((result) => (
        <div key={result.id}>
          <h2>{result.title}</h2>
          <p>{result.content}</p>
        </div>
      ))}
    </div>
  );
};

export default Displayer;
