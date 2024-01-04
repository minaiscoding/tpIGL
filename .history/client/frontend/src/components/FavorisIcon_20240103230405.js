import { useState } from "react";
import React from 'react';
import axios from "axios";
import { BsBookmarks } from "react-icons/bs";
import { BsBookmarksFill } from "react-icons/bs";



const FavorisIcon = ({ articleId, user_id }) => {
 
  const [favoris, setFavoris] = useState(false);
  const style = "size-10 text-yellow";

 const addToFavorites = async () => {
   try {
     const token = localStorage.getItem("token");
     const response = await axios.post(
       "http://127.0.0.1:8000/api/save-favorite/",
       {
         articleId: articleId,
         userId: user_id,
       },
       {
         headers: {
           Authorization: `Bearer ${token}`,
         },
       }
     );
     if (response.status === 200) {
       setFavoris(true);
     }
   } catch (error) {
     console.error("Error saving favorite article:", error);
   }
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
