import React, { useState, useEffect } from "react";
import axios from "axios";
// ADD AN ONCHANGE FUNCTION FOR THE EDIT FORM
// ADD HANDLE SUBLIT FOR THE BUTTON SAVE (INTEGRAION FCTN)
// ADD CANCEL INTEGRATION FNCTION

const style1 = "font-Futura text-left text-xl text-purple2 font-semibold";
const style2 = "font-Futura text-navBg text-base text-wrap ml-2 mb-2";
const style3 =
  "font-Futura text-navBg text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md w-[90%] w-full ";

function InfoArticle(props) {
  const [formData, setFormData] = useState({ ...props.article });
  const [loading, setLoading] = useState(true);
  const [articleData, setArticleData] = useState(null);


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };




  return (
    <div
      className={`bg-[#ffff] mx-4 border-solid rounded-sm px-8 py-2 max-h-[75%] border-navBg mt-20 sm:mt-8 mb-4 w-[85%]`}
    >
      {props.edit ? (
        <div className="flex flex-col items-start text-left gap-2">
          <label htmlFor="titre" className={style1}>
            {" "}
            Titre de l'article :
          </label>
          <input
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
          <h2 className={style1}> Titre de l'article :</h2>
          <p className={style2}>{formData.Titre}</p>

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
  );
}

export default InfoArticle;
