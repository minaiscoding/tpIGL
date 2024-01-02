import { useState } from "react";
import React from 'react';
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";

const FavorisIcon = () => {
    const [favoris, setFavoris] = useState(false);
    const  style ='size-10 text-yellow';

    const addToFavorites = (props) => {
        // Integration
       
        setFavoris(true);
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
