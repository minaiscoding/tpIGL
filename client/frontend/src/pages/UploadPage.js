import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import Navbar from "../components/NavBar"; // Import your Navbar component
import add from "../../src/file_upload_icon.svg";
import link from "../../src/url_icon.svg";
import vector_bg from "../../src/Vector.svg";



const UploadPage = () => {
  const backgroundImage = `url(${vector_bg})`;
  const acceptedFileTypes = ".pdf";
  const onDrop = useCallback((acceptedFiles) => {
  console.log("Accepted Files:", acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes,
  });

  return (
    <div
     style={{ backgroundImage }}
     
      className="h-full w-screen min-h-screen font-Futura bg-cover bg-center flex flex-col"
     >
      {/* Navbar Component */}
         <Navbar />
      <div
       className="h-full w-screen flex flex-col items-center justify-center font-Futura"
       >
        <p 
         className="text-3xl flex flex-col  items-center justify-center font-Futura-bold pb-8 mt-20"
         >Upload article</p>
      </div>
      <div
      className="items-center justify-center flex flex-col"  
      >
      <div {...getRootProps()}
        className="w-[80%] px-4 py-2 flex flex-col items-center border-2  border-dashed  border-gray-900  rounded-lg cursor-pointer text-center  ml-2 mr-2 pt-6 pl-6 pb-6 pr-6 bg-gradient-to-b from-purple-600 to-purple-600"
      >
        <input {...getInputProps()} />
        <img  
         className=" w-20 mb-5 mt-5  " src={add} alt="upload_file_icon" />

        {isDragActive ? (
          <div>
            <p
             className="pb-8 text-2xl font-Futura"
             >Dropez vos fichiers ici...</p>
          </div>
        ) : (
          <div>
            <p 
             className="pb-8 text-2xl font-Futura">
              Déposez votre fichier ici ou<br/>parcourez pour le sélectionner
            </p>
          </div>
        )}
      </div>
      <div 
       className="w-[80%]  text-black  px-4 py-2 mt-10 flex flex-col border  border-black rounded-md  relative bg-gradient-to-b from-purple-600 to-purple-600 mb-32 sm:mb-40 md:mb-48 lg:mb-56 xl:mb-64"
       >
  <input
    type="url"
    placeholder="Enter URL"
    className="text-2xl font-Futura bg-transparent border-none focus:outline-none placeholder-gray-500 pl-4"

  />
  <img
    src={link}
    alt="Link Icon"
    className="absolute right-4 top-1/2 transform -translate-y-1/2 h-6 w-6"
  />
</div>
</div>
</div>
  );
};
export default UploadPage;