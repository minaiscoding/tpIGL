
import React, { useState, useEffect } from "react";
import vector_bg from "../assets/Vector.svg";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { IoArrowBack } from "react-icons/io5";




const DetailsArticle = ({ role }) => {
  const style1 = "font-Futura text-left text-2xl text-purple2 font-semibold";
  const style2 = "font-Futura text-navBg text-base text-wrap ml-2 mb-2  max-w-full text-wrap";
  const style3 =
    "font-Futura text-navBg  text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md  w-[90%] w-full  max-w-full text-wrap ";

  const backgroundImage = `url(${vector_bg})`;
  const [edit, setEdit] = useState(false);
  const [articleData, setArticleData] = useState(null);
  const [formData, setFormData] = useState(null);
  const articleId = useParams();
  const nav = useNavigate();
  

  useEffect(() => {
    // Fetch articles when the component mounts
    fetchArticles();
  }, []);




  const fetchArticles = async () => {
    try {
      console.log ('hello');
      console.log ('*****',articleId.articleId);
      const response = await axios.get(
        `http://localhost:8000/api/articles/${articleId.articleId}`

      );
      console.log (response);
      console.log ('hello');
      console.log (response.data);

      
      setFormData(response.data);
      setArticleData(response.data);
      console.log (response);
      console.log ('hello');
      console.log (response.data);

      
      setFormData(response.data);
      setArticleData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleModifier = () => {
    setEdit(true);
  };



  const handleAnnuler = () => {
    setFormData(articleData);
    setEdit(false);
  };

  const handleDelete = async () => {
    try {
      // Retrieve the article ID from local storage


      const response = await axios.delete(
        `http://localhost:8000/api/articles/${articleId.articleId}`        
        `http://localhost:8000/api/articles/${articleId.articleId}`        
      );

      // Check the response and handle accordingly
      if (response.status === 200) {
        console.log("Document deleted successfully from Elasticsearch");
        nav('/articles');
        toast.success(`l'article est supprimé avec succès`);

        // Optionally, update the state or perform other actions
      } else {
        console.error("Failed to delete document from Elasticsearch");
        toast.error(`Error l'article n'est pas supprimé.`);
      }
    } catch (error) {
      console.error("Error deleting document:", error);
    }
  };

  const handleUpdate = async () => {
    try {
        const response = await axios.put(
            `http://localhost:8000/api/articles/${articleId.articleId}/`,
            formData
        );
        
        if (response.status === 200) {
            console.log("Document updated successfully in Elasticsearch");
            setEdit(false);
            toast.success(`Article updated successfully`);
        } else {
            console.error("Failed to update document in Elasticsearch", response);
            toast.error(`Failed to update article`);
        }
    } catch (error) {
        console.error("Error updating document:", error);
        toast.error(`Error updating article: ${error.message}`);
    }
};


  return (
    <div
      style={{ backgroundImage }}
      className="w-screen h-full min-h-screen bg-purple300 bg-center bg-no-repeat flex flex-col items-center justify-center px-2 bg-cover pb-8 overflow-y-scroll max-w-screen"
    >

      {articleData ? (
        <>
          <div
            className="flex flex-row gap-1 absolute left-2 top-8 sm:top-[70px] cursor-pointer"
            onClick={() =>edit ? nav(`/details/${articleId.articleId}`) :edit ? nav(`/details/${articleId.articleId}`) : nav("/articles")}
          >
            <IoArrowBack className=" text-white size-6   " />
            <p className=" font-Futura text-white text-md font-bold  " >Retour</p>
          </div>
          <div
            className={`bg-[#ffff] mx-4 border-solid rounded-sm px-8 py-2 max-h-[75%] border-navBg mt-20 sm:mt-8 mb-4 w-[90%]`}
          >
            {edit ? (
              <div className="flex flex-col items-start text-left gap-2">
                <label
                  htmlFor="titre"
                  className="font-Futura text-left text-2xl text-purple2 font-semibold"
                >
                  {" "}
                  Titre de l'article :
                </label>
                <textarea
                  type="text"
                  id="titre"
                  name="Titre"
                  value={formData.Titre}
                  onChange={handleChange}
                  className={style3}
                />

                <label htmlFor="auteurs" className={style1}>
                  Les auteurs :
                </label>
                <textarea
                  type="text"
                  id="auteurs"
                  name="auteurs"
                  value={formData.auteurs}
                  onChange={handleChange}
                  className={style3}
                />

                <label htmlFor="institutions" className={style1}>
                  {" "}
                  Institusions :
                </label>
                <textarea
                  type="text"
                  id="institutions"
                  name="Institution"
                  value={formData.Institution}
                  onChange={handleChange}
                  className={style3}
                />

                <label htmlFor="resume" className={style1}>
                  {" "}
                  Résumé :
                </label>
                <textarea
                  type="text"
                  id="resume"
                  name="Resume"
                  value={formData.Resume}
                  onChange={handleChange}
                  className={`${style3} h-[300px] `}
                />

                <label htmlFor="motsCles" className={style1}>
                  {" "}
                  Mots clés :
                </label>
                <textarea
                  type="text"
                  id="motsCles"
                  name="MotsCles"
                  value={formData.MotsCles}
                  onChange={handleChange}
                  className={style3 }
                />

                <label htmlFor="texte" className={style1}>
                  {" "}
                  Texte :
                </label>
                <textarea
                  type="text"
                  id="texte"
                  name="text"
                  value={formData.text}
                  onChange={handleChange}
                  className={`${style3} h-screen `}
                />

                <label htmlFor="biblio" className={style1}>
                  {" "}
                  Bibiliographie :
                </label>
                <textarea
                  type="text"
                  id="biblio"
                  name="RefBib"
                  value={formData.RefBib}
                  onChange={handleChange}
                  className={`${style3} h-[300px] `}
                />
              </div>
            ) : (
              <div className="flex flex-col items-start justify-center text-left max-w-screen ">
                <h2 className="font-Futura text-left text-2xl text-purple2 font-semibold">
                  {" "}
                  Titre de l'article :
                </h2>
                <p className="font-Futura text-navBg text-base text-wrap ml-2 mb-2">
                  {formData.Titre}
                </p>

                <h2 className={style1}>Les auteurs :</h2>
                <p className={style2}>{formData.auteurs}</p>

                <h2 className={style1}> Institusions :</h2>
                <p className={style2}>{formData.Institution}</p>

                <h2 className={style1}> Résumé :</h2>
                <p className={style2}>{formData.Resume}</p>

                <h2 className={style1}> Mots clés : </h2>
                <p className={style2}>{formData.MotsCles}</p>

                <h2 className={style1}> Texte :</h2>
                <p className={`${style2} ml-2 `}>{formData.text}</p>

                <h2 className={style1}> Bibiliographie : </h2>
                <p className={`${style2} ml-2 `}>{formData.RefBib}</p>
              </div>
            )}
          </div>

          {role === "moderator" && (
            <div className="flex flex-row justify-center gap-4 md:gap-12 lg:gap-16 xl:gap-24">
              <ToastContainer />
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
                    onClick={handleUpdate}
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
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default DetailsArticle;