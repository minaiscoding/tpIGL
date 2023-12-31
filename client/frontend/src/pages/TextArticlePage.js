import React, { useState, useEffect } from "react";
import vector_bg from "../assets/Vector.svg";
import pdf_img from "../assets/pdf.png"
import axios from "axios";
import { useParams } from "react-router";

export const TextArticlePage = () => {
    const backgroundImage = `url(${vector_bg})`;
    const [articleData, setArticleData] = useState(null);
    const [url, setUrl] = useState("");


    useEffect(() => {
        // Fetch articles when the component mounts
        fetchArticles();
    }, []);

    const articleId =useParams ();


    const fetchArticles = async () => {
        try {
            const response = await axios.get( `http://localhost:9200/articles/_doc/SILvsYwByJ8brC2scB_6`);
            const fetchedArticles = response.data._source;

            setArticleData({ ...fetchedArticles});
            setUrl(fetchedArticles.URL_Pdf);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleRetourClick = () => {
        // Navigate back to the previous page
        window.history.back();
    };

    return (
        <div
            style={{ backgroundImage }}
            className=" relative w-screen h-screen min-h-screen bg-purple300  bg-center bg-no-repeat flex flex-col items-center justify-center px-2 bg-cover pb-8"
        >
            {articleData ? (

                <>
                    <a href={url}>  <img src={pdf_img} className=" absolute top-16 sm:top-2 z-50 left-4 w-[5%] " /></a>
                    <div
                        className={`  bg-[#ffff] mx-4 border-solid rounded-sm px-8 py-2 h-[95vh] border-navBg mt-20 sm:mt-8 mb-4 w-[95%]   overflow-y-scroll`}
                    >
                        <p className='font-Futura text-navBg text-base text-wrap ml-2 mb-2'>{articleData.text}</p>
                    </div>
                    <div className="flex flex-row justify-center ">
                        <button
                            className="bg-navBg text-lg font-Futura text-[#fff] text-center rounded-sm px-6 md:px-12 py-2"
                            onClick={handleRetourClick}
                        >
                            Retour
                        </button>
                    </div>
                </>


            ) : (
                <p>Loading...</p>
            )
            }

        </div >
    )
}
