import React, { useState, useEffect } from "react";
import vector_bg from "../assets/Vector.svg";
import axios from "axios";
import { useNavigate } from "react-router-dom";



const DetailsArticle = ({ role }) => {
    const style1 = "font-Futura text-left text-xl text-purple2 font-semibold";
    const style2 = "font-Futura text-navBg text-base text-wrap ml-2 mb-2";
    const style3 =
        "font-Futura text-navBg text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md w-[90%] w-full ";

    const backgroundImage = `url(${vector_bg})`;
    const [edit, setEdit] = useState(false);
    const [articleData, setArticleData] = useState(null);
    const [formData, setFormData] = useState(null);

    useEffect(() => {
        // Fetch articles when the component mounts
        fetchArticles();
    }, []);

   


    const fetchArticles = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/api/articles/`);
            const fetchedArticles = response.data;
            setFormData(fetchedArticles[1] || {});
            setArticleData({ ...fetchedArticles[1] });
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

    const handleEnregistrer = () => {
        console.log("Save button clicked");
        console.log(formData); // FormData is available here for further processing
        // Add your logic to send the formData to the server or perform any other actions
        setEdit(false);
    };

    const handleAnnuler = () => {
        setFormData(articleData);
        setEdit(false);
    };

    const handleDelete = async () => {
        try {
            console.log("Article Data:", articleData);

            if (articleData && articleData.id) {
                const response = await axios.delete(
                    `http://localhost:8000/api/articles/${articleData.id}/`
                );

                console.log("Delete Response:", response.data);

                if (response.status === 204) {
                    console.log("Article deleted successfully");
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
                <>
                    <div
                        className={`bg-[#ffff] mx-4 border-solid rounded-sm px-8 py-2 max-h-[75%] border-navBg mt-20 sm:mt-8 mb-4 w-[90%]`}
                    >
                        {edit ? (
                            <div className="flex flex-col items-start text-left gap-2">
                                <label htmlFor="titre" className="font-Futura text-left text-xl text-purple2 font-semibold">
                                    {" "}
                                    Titre de l'article :
                                </label>
                                <input
                                    type="text"
                                    id="titre"
                                    name="Titre"
                                    value={formData.Titre}
                                    onChange={handleChange}
                                    className="font-Futura text-navBg text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md w-[90%] w-full"
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
                                    className={style3}
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
                                    className={style3}
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
                                    className={style3}
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
                                    className={style3}
                                />

                            </div>
                        ) : (
                            <div className="flex flex-col items-start justify-center text-left">
                                <h2 className="font-Futura text-left text-xl text-purple2 font-semibold"> Titre de l'article :</h2>
                                <p className="font-Futura text-navBg text-base text-wrap ml-2 mb-2">{formData.Titre}</p>

                                <h2 className={style1}>Les auteurs :</h2>
                                <p className={style2}>{formData.auteurs}</p>

                                <h2 className={style1}> Institusions :</h2>
                                <p className={style2}>{formData.Institution}</p>

                                <h2 className={style1}> Résumé :</h2>
                                <p className={style2}>{formData.Resume}</p>

                                <h2 className={style1}> Mots clés : </h2>
                                <p className={style2}>{formData.MotsCles}</p>

                                <h2 className={style1}> Texte :</h2>
                                <p className={`${style2} ml-2`}>{formData.text}</p>

                                <h2 className={style1}> Bibiliographie : </h2>
                                <p className={`${style2} ml-2`}>{formData.RefBib}</p>

                            </div>
                        )}
                    </div>


                    {role === "moderator" || role === "admin" && (
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
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default DetailsArticle;
