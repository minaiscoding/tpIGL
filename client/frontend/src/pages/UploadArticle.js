import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import FileUpload from "../components/FileUpload";
import link from "../../src/url_icon.svg";
import vector_bg from "../../src/Vector.svg";

const UploadArticle = () => {
  // Background image style
  const backgroundImage = `url(${vector_bg})`;

  // State for selected files and URL input
  const [files, setFiles] = useState([]);
  const [url, setUrl] = useState("");


  function delay(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
  }

  // Function to handle file upload
  const handleFileUpload = async () => {
    let response = null;
    try {
      if (files.length === 0) {
        return;
      }

      // Check if there are any non-PDF files
      const nonPdfFiles = files.filter((file) => file.type !== 'application/pdf');
      if (nonPdfFiles.length > 0) {
        const nonPdfFileNames = nonPdfFiles.map((file) => file.name).join(', ');
        //alert(`Invalid file(s): ${nonPdfFileNames}. Only PDF files are accepted.`);
        toast.error(`fichier(s) invalide(s): ${nonPdfFileNames}. que des fichiers PDF qui sont acceptés.`);
        return;
      }

      // Iterate through each file and upload individually
      for (const file of files) {
        const formData = new FormData();
        
        formData.append('pdf_File', file);

        response = await axios.post(
          'http://127.0.0.1:8000/api/articles_ctrl/local-upload/',
          formData,
        );
       // console.log('File uploaded successfully:', response.data);
       // alert(`File ${file.name} uploaded successfully`);
       toast.success(`Article ${file.name}: ${response.data.url_pdf} est joint avec succès`);
        console.log("Article est joint avec succès:", response.data);
      }

      //alert('All files uploaded successfully');
      await delay(3);
      toast.success("tout les articles séléctionés sont joints avec succès");
    } catch (error) {
      console.error('Erreur uploading:', error.message);
      const errorMessage = error.response?.data?.error || error.message;
      //alert(`Erreur uploading: ${errorMessage}`);
      // Display specific error message from the backend, if available
      if (error.response?.data?.error) {
         toast.error(`Erreur uploading fichiers: ${error.response.data.error}`);
      } else {
        toast.error(`Error uploading fichiers: ${errorMessage}`);
      }
    } finally {
      setFiles([]);
    }
  };

  const handleUrlSubmit = async () => {
    let response = null;
    try {
      if (!url) {
        return;
      }

      const formData = new FormData();
      formData.append("URL_Pdf", url);

      response = await axios.post(
        "http://127.0.0.1:8000/api/articles_ctrl/external-upload/",
        formData
      );

      console.log("Article est joint avec succès d'après l'url:", response.data);
      toast.success(`Article est joint avec succès d'après l'url ${url}`);
      //alert("URL submitted successfully");
    } catch (error) {
      console.error("Erreur submitting URL:", error.message);
      const errorMessage = error.response?.data?.error || error.message;

      if (error.response?.data?.error) {
        toast.error(`Erreur submitting URL: ${error.response.data.error}`);
      } else {
        toast.error(`Erreur submitting URL: ${errorMessage}`);
      }
    } finally {
      setUrl("");
    }
  };

  return (
    <div>
      {/* Main container with background image */}
      <div
        style={{ backgroundImage }}
        className="h-full w-screen min-h-screen font-Futura bg-cover bg-center flex flex-col"
      >
       
        <div className="h-full w-screen flex flex-col items-center justify-center font-Futura">
          {/* Header */}
          <p className="text-3xl flex flex-col items-center justify-center font-Futura-bold pb-8 mt-20">
            Upload article
          </p>
        </div>

        <div className="items-center justify-center flex flex-col">
          {/* Use the FileUpload component */}
          <FileUpload
            handleFileUpload={handleFileUpload}
            files={files}
            setFiles={setFiles}
          />
           <ToastContainer />
          {/* URL input */}
          <div className="w-[80%] text-black px-4 py-2 mt-10 flex flex-col border-2 border-black rounded-rd relative bg-gradient-to-b from-purple-600 to-purple-600 mb-32 sm:mb-40 md:mb-48 lg:mb-56 xl:mb-64 transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-300">
            <input
              type="url"
              placeholder="Enter URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="text-2xl font-Futura  bg-transparent border-none focus:outline-none placeholder-gray-900 pl-4 bg-gradient-to-b from-purple-600 to-purple-600 "
            />
            <img
              src={link}
              alt="Link Icon"
              onClick={handleUrlSubmit}
              className="cursor-pointer absolute right-4 top-1/2 transform -translate-y-1/2 h-6 w-6"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadArticle;
