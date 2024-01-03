// Displayer.js

import React, { useEffect, useState } from "react";

const Displayer = ({ results }) => {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const getRandomUserId = async () => {
      try {
        const response = await fetch('/api/get-random-user/');
        if (response.ok) {
          const data = await response.json();
          setUserId(data.user_id);
        } else {
          console.error('Error fetching random user ID:', response.status);
        }
      } catch (error) {
        console.error('Error fetching random user ID:', error);
      }
    };

    getRandomUserId();
  }, []);  // The empty dependency array ensures that this effect runs once when the component mounts

  // ... (other code)

  return (
    <div>
      {results.map((result) => (
        <div
          key={result.Titre}
          className="bg-white border border-black rounded-md p-4 mb-4 result-container"
          style={{ display: "flex", flexDirection: "column" }}
        >
          <div style={{ alignSelf: "flex-end" }}>
            {userId !== null && (
              <FavorisIcon user_id={userId} articleId={result.id} />
            )}
          </div>
          <h2>{result.Titre}</h2>
          <p>{result.Resume}</p>
          <p>{result.id}</p>
        </div>
      ))}
    </div>
  );
};

export default Displayer;
