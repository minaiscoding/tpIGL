import React from "react";

const FavoriePage = () => {
    return (
      <div>
        <h1>Data Page</h1>
        {/* Use the DataDisplay component with a specific endpoint */}
        <DataDisplay endpoint="utilisateurs" />
        <DataDisplay endpoint="articles" />
        <DataDisplay endpoint="favoris" />
      </div>
    );
  };


export default FavoriePage;