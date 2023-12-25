import React from 'react';



// ADD AN ONCHANGE FUNCTION FOR THE EDIT FORM
// ADD HANDLE SUBLIT FOR THE BUTTON SAVE (INTEGRAION FCTN)
// ADD CANCEL INTEGRATION FNCTION


const info = {
  titre: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
  auteurs: "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  institutions: "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
  resume: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
  motsCles: "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  texte: "Some random text for the article content. Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
  biblio: "More random text for the bibliography. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
};

const style1 = 'font-Futura text-left text-xl text-purple2 font-semibold';
const style2 = 'font-Futura text-navBg text-base text-wrap ml-2 mb-2';
const style3 ='font-Futura text-navBg text-base text-wrap ml-2 mb-2 border-solid border-[1px] border-navBg px-2  rounded-md w-[90%] w-full ';

function InfoArticle(props) {

  return (
    <div className={`bg-white mx-4 border-solid rounded-sm px-8 py-2 max-h-[75%] border-navBg  mt-20 sm:mt-8  mb-4 w-[85%]`}>
      {!props.edit ? (
        <div className='flex flex-col items-start justify-center text-left'>
          <h2 className={style1}> Titre de l'article :</h2>
          <p className={style2}>{info.titre}</p>

          <h2 className={style1}>Les auteurs :</h2>
          <p className={style2}>{info.auteurs}</p>

          <h2 className={style1}> Institusions :</h2>
          <p className={style2}>{info.institutions}</p>

          <h2 className={style1}> Résumé :</h2>
          <p className={style2}>{info.resume}</p>

          <h2 className={`${style1} ml-2`}> Mots clés : </h2>
          <p className={style2}>{info.motsCles}</p>

          <h2 className={style1}> Texte :</h2>
          <p className={`${style2} ml-2`}>{info.texte}</p>

          <h2 className={style1}> Bibiliographie : </h2>
          <p className={`${style2} ml-2`}>{info.biblio}</p>
        </div>
      ) : (
        <div className='flex flex-col items-start text-left gap-2  '>
         
            <label htmlFor='titre' className={style1}> Titre de l'article :</label>
            <input type='text' id='titre' name='titre'  rows={5} defaultValue={info.titre} className={style3} />

            <label htmlFor='auteurs' className={style1}>Les auteurs :</label>
            <textarea type='text' id='auteurs' name='auteurs'  rows={5} defaultValue={info.auteurs} className={style3} />

            <label htmlFor='institutions' className={style1}> Institusions :</label>
            <textarea type='text' id='institutions' name='institutions'  rows={5} defaultValue={info.institutions} className={style3} />

            <label htmlFor='resume' className={style1}> Résumé :</label>
            <textarea type='text' id='resume' name='resume' defaultValue={info.resume} className={style3} />

            <label htmlFor='motsCles' className={style1}> Mots clés : </label>
            <textarea type='text' id='motsCles' name='motsCles' defaultValue={info.motsCles} className={style3} />

            <label htmlFor='texte' className={style1}> Texte :</label>
            <textarea type='text' id='texte' name='texte'  rows={5} defaultValue={info.texte} className={style3} />

            <label htmlFor='biblio' className={style1}> Bibiliographie : </label>
            <textarea type='text' id='biblio' name='biblio'   rows={5} defaultValue={info.biblio} className={style3} />
          
        </div>
      )}
    </div>
  );
}

export default InfoArticle;
