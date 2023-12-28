import React, { useState, useEffect } from "react";
import vector_bg from "../assets/Vector.svg";
import InfoArticle from "../components/InfoArticle";
import axios from "axios";

const DetailsArticle = () => {
  const backgroundImage = `url(${vector_bg})`;
  const [edit, setEdit] = useState(false);
  const [role, setRole] = useState("modérateur");
  const [articleData, setArticleData] = useState(null);
  const [formData, setFormData] = useState(null);

  useEffect(() => {
    // Fetch article data from the API
    const fetchArticleData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/articles/BFxWoYwBWAlgPuQlUZBw"
        ); // Replace with your API endpoint
        const data = await response.json();
        setArticleData(data);
        setFormData(data); // Set initial form data
      } catch (error) {
        console.error("Error fetching article data:", error);
      }
    };

    fetchArticleData();
  }, []); // Empty dependency array ensures the effect runs only once when the component mounts

  const handleModifier = () => {
    setEdit(true);
    setFormData(articleData);
  };

  const handleEnregistrer = () => {
    // Implement the save functionality using formData
    console.log("Save button clicked");
    console.log(formData); // FormData is available here for further processing
    // Add your logic to send the formData to the server or perform any other actions
    setEdit(false);
  };

  const handleAnnuler = () => {
    setEdit(false);
    // Reset form data to the original article data when cancelling
    setFormData(articleData);
  };

  const handleDelete = async () => {
    try {
      console.log("Article Data:", articleData);

      if (articleData && articleData.id) {
        const response = await axios.delete(
          `http://localhost:8000/api/articles/${articleData.id}/`
        );

        console.log("Delete Response:", response.data); // Log the delete response

        if (response.status === 204) {
          console.log("Article deleted successfully");
          // Add any additional logic after deletion if needed
        } else {
          console.error(
            "Delete request was not successful. Status:",
            response.status
          );
        }
      } else {
        console.error("Invalid article data or missing ID");
      }
    } catch (error) {
      console.error("Error deleting article:", error);
    }
  };

  return (
    <div
      style={{ backgroundImage }}
      className="w-screen h-full min-h-screen bg-purple-3OO bg-center bg-no-repeat flex flex-col items-center justify-center px-2 bg-cover pb-8 overflow-y-scroll"
    >
      {articleData ? (
        <InfoArticle edit={edit} article={formData} />
      ) : (
        <p>Loading...</p>
      )}

      {role === "modérateur" && (
        <div className="flex flex-row justify-center gap-4 md:gap-12 lg:gap-16 xl:gap-24">
          {!edit ? (
            <>
              <button
                className="bg-[#ffff] text-lg font-Futura text-navBg text-center rounded-sm px-6 md:px-12 py-2"
                onClick={handleModifier}
              >
                Modifier
              </button>
              <button
                className="bg-[#6B30E4] text-lg font-Futura text-[#fff] text-center rounded-sm px-6 md:px-12 py-2"
                onClick={handleDelete}
              >
                Supprimer
              </button>
            </>
          ) : (
            <>
              <button
                className="bg-[#6B30E4] text-lg font-Futura text-[#fff]text-center rounded-sm px-6 md:px-12 py-2"
                onClick={handleEnregistrer}
              >
                Enregistrer
              </button>
              <button
                className="bg-yellow text-lg font-Futura text-[#fff] text-center rounded-sm px-6 md:px-12 py-2"
                onClick={handleAnnuler}
              >
                Annuler
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default DetailsArticle;
