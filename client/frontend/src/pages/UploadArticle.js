import React, { useCallback, useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

import add from "../../src/file_upload_icon.svg";
import link from "../../src/url_icon.svg";
import vector_bg from "../../src/Vector.svg";
//import { CheckCircleIcon, FileIcon } from 'lucide-react';

const UploadArticle = () => {
  const backgroundImage = `url(${vector_bg})`;
  const acceptedFileTypes = ".pdf";

  const [files, setFiles] = useState([]);
  const [url, setUrl] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
  }, []);

  const handleUpload = async () => {
    try {
      setUploadError(null);

      const uploadPromises = files.map(async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        // Upload file
        const response = await axios.post(
          "http://127.0.0.1:8000/api/articles_ctrl/local-upload/",
          formData,
          {
            onUploadProgress: (progressEvent) => {
              const progress = Math.round(
                (progressEvent.loaded / progressEvent.total) * 100
              );
              setUploadProgress(progress);
            },
          }
        );

        console.log(`File ${file.name} uploaded successfully:`, response.data);
      });

      // if the URL field is not empty
      if (url) {
        await axios.post(
          "http://127.0.0.1:8000/api/articles_ctrl/external-upload/",
          { url }
        );

        console.log("URL uploaded successfully");
      }

      // Wait for all file uploads to complete before displaying success messages
      await Promise.all(uploadPromises);

      // Handle success, e.g., show a success message to the user
      console.log("Upload successful!");
    } catch (error) {
      // Handle error, e.g., show an error message to the user
      console.error("Error uploading file:", error.message);
      setUploadError("Error uploading file. Please try again.");
    } finally {
      // Reset progress after upload completion
      setUploadProgress(0);
      // Clear uploaded files
      setFiles([]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes,
  });

  const handleDropZoneKeyPress = (event) => {
    // Check if the key pressed is Enter
    if (event.key === "Enter") {
      handleUpload();
    }
  };

  const handleUrlKeyPress = (event) => {
    // Check if the key pressed is Enter
    if (event.key === "Enter") {
      handleUpload();
    }
  };

  return (
    <div
      style={{ backgroundImage }}
      className="h-full w-screen min-h-screen font-Futura bg-cover bg-center flex flex-col"
    >
      

      <div className="h-full w-screen flex flex-col items-center justify-center font-Futura">

        <p className="text-3xl flex flex-col items-center justify-center font-Futura-bold pb-8 mt-20">
          Upload article
        </p>

      </div>

      <div className="items-center justify-center flex flex-col">

        {/* Dropzone for file upload */}
        <div
          {...getRootProps() }
          onKeyDown={handleDropZoneKeyPress}
          tabIndex={0}
          className="w-[80%] dropzone px-4 py-2 flex flex-col items-center border-2 border-dashed border-black rounded-rd cursor-pointer text-center ml-2 mr-2 pt-6 pl-6 pb-6 pr-6 bg-gradient-to-b from-purple-600 to-purple-600 relative transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-300"
          >
          <input {...getInputProps()} />
          <img className="w-20 mb-5 mt-5" src={add} alt="upload_file_icon" />

          {isDragActive ? (

            <div>
              <p className="pb-8 text-2xl font-Futura">Dropez vos fichiers ici...</p>
            </div>

          ) : (

            <div>
              <p className="pb-8 text-2xl font-Futura">
                Déposez votre fichier ici ou<br />parcourez pour le sélectionner
              </p>
            </div>

          )}

        </div>

        <div
          className="w-[80%]  text-black  px-4 py-2 mt-10 flex flex-col border  border-black rounded-rd  relative bg-gradient-to-b from-purple-600 to-purple-600 mb-32 sm:mb-40 md:mb-48 lg:mb-56 xl:mb-64  transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-300"
        >
          <input
            type="url"
            placeholder="Enter URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={handleUrlKeyPress}
            className="text-2xl font-Futura bg-transparent border-none focus:outline-none placeholder-gray-500 pl-4 bg-gradient-to-b from-purple-600 to-purple-600 "
          />
          <img
            src={link}
            alt="Link Icon"
            className="absolute right-4 top-1/2 transform -translate-y-1/2 h-6 w-6"
          />

        </div>
        {files.length > 0 && (
        <div>
          <h2>Selected Files</h2>
          <ul>
            {files.map((file) => (
              <li key={file.name}>
                {file.name} - {file.size} bytes
              </li>
            ))}
          </ul>
        </div>
      )}
      {uploadProgress > 0 && (
        <div>
          <h2>Upload Progress: {uploadProgress}%</h2>
          <progress value={uploadProgress} max="100" />
        </div>
      )}
      {uploadError && <div>Error: {uploadError}</div>}
      <button onClick={handleUpload}>Upload</button>

      </div>

    </div>
  );
};

export default UploadArticle;
