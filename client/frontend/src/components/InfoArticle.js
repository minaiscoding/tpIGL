import React from "react";

// ADD AN ONCHANGE FUNCTION FOR THE EDIT FORM
// ADD HANDLE SUBLIT FOR THE BUTTON SAVE (INTEGRAION FCTN)
// ADD CANCEL INTEGRATION FNCTION

const info = {
  titre: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
  auteurs: "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  institutions:
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
  resume:
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
  motsCles:
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  texte:
    "Some random text for the article content. Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
  biblio:
    "More random text for the bibliography. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
};

const style1 = "font-Futura text-left text-xl text-purple2 font-semibold";
const style2 = "font-Futura text-navBg text-base text-wrap ml-2 mb-2";
const style3 =
  "font-Futura text-navBg text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md w-[90%] w-full ";

function InfoArticle(props) {
  const [formData, setFormData] = useState(props.article || {});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (props.edit) {
      // Update form data when 'edit' prop changes
      setFormData(props.article || {});
    } else {
      // Fetch articles when component mounts
      fetchArticles();
    }
  }, [props.edit, props.article]);

  const fetchArticles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/articles");
      const fetchedArticles = response.data;
      setFormData(fetchedArticles[1] || {}); // Assuming you want to display the first article
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:8000/api/articles/${formData.id}`);
      // Assuming that the server returns a success status (2xx)
      // You may want to handle different response status codes appropriately
      console.log("Article deleted successfully");
      // Add any additional logic after deletion if needed
    } catch (error) {
      console.error("Error deleting article:", error);
    }
  };

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
            name="titre"
            value={formData.Titre || ""}
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
            value={formData.auteurs || ""}
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
            name="institutions"
            value={formData.Institution || ""}
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
            name="resume"
            value={formData.Resume || ""}
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
            name="motsCles"
            value={formData.MotsCles || ""}
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
            name="texte"
            value={formData.text || ""}
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
            name="biblio"
            value={formData.RefBib || ""}
            onChange={handleChange}
            className={style3}
          />

          <button
            className="bg-[#6B30E4] text-lg font-Futura text-[#fff] text-center rounded-sm px-6 md:px-12 py-2"
            onClick={() => {
              console.log("Save button clicked");
              console.log(formData);
            }}
          >
            Enregistrer
          </button>
          <button
            className="bg-yellow text-lg font-Futura text-[#fff] text-center rounded-sm px-6 md:px-12 py-2"
            onClick={() => {
              console.log("Cancel button clicked");
              // props.setEdit(false);
            }}
          >
            Annuler
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-start justify-center text-left">
          <h2 className={style1}> Titre de l'article :</h2>
          <p className={style2}>{formData.Titre || ""}</p>

          <h2 className={style1}>Les auteurs :</h2>
          <p className={style2}>{formData.auteurs || ""}</p>

          <h2 className={style1}> Institusions :</h2>
          <p className={style2}>{formData.Institution || ""}</p>

          <h2 className={style1}> Résumé :</h2>
          <p className={style2}>{formData.Resume || ""}</p>

          <h2 className={`${style1} ml-2`}> Mots clés : </h2>
          <p className={style2}>{formData.MotsCles || ""}</p>

          <h2 className={style1}> Texte :</h2>
          <p className={`${style2} ml-2`}>{formData.text || ""}</p>

          <h2 className={style1}> Bibiliographie : </h2>
          <p className={`${style2} ml-2`}>{formData.RefBib || ""}</p>
        </div>
      )}
    </div>
  );
}

export default InfoArticle;
