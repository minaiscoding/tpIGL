import { useState } from "react";
import React from 'react';
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = () => {
    const [favoris, setFavoris] = useState(false);
    const  style ='size-8 text-yellow';

    const addToFavorites = (props) => {
        axios
          .post("http://localhost:8000/favorite-articles/", {
            article: articleId,
          })
          .then((response) => {
            setFavoris(true);
          })
          .catch((error) => {
            console.error("Error saving favorite article:", error);
          });
       
        
    };

    const deleteFromFavorites = () => {
       // Integration 
        setFavoris(false);
    };

    return (
        <div>
            {favoris ? (
                <BsBookmarksFill className={style} onClick={deleteFromFavorites} />
            ) : (
                <BsBookmarks className={style} onClick={addToFavorites} />
            )}
        </div>
    );
};

export default FavorisIcon;
