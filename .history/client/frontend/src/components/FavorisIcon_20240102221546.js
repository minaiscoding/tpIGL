import { useState } from "react";
import React from "react";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = (}) => {
  const [favoris, setFavoris] = useState(false);
  const style = "size-8 text-yellow";

  const addToFavorites = (props) => {
    // Integration

    setFavoris(true);
  };

  return (
    <div>
      {favoris ? (
        <BsBookmarksFill className={style} />
      ) : (
        <BsBookmarks className={style} onClick={addToFavorites} />
      )}
    </div>
  );
};

export default FavorisIcon;
