// FileUpload.js
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FileIcon, Trash2Icon } from 'lucide-react';
import add from '../../src/file_upload_icon.svg';

const FileUpload = ({ handleFileUpload, files, setFiles }) => {
  // Callback for handling dropped files
  const onDrop = useCallback((acceptedFiles) => {
    // Update the state with the new files
    setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
  }, [setFiles]);

  // Function to remove a file from the list
  const removeFile = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
  };

  // Dropzone configuration
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: '.pdf',
  });

  return (
    <>
      {/* Dropzone for file upload */}
      <div
        {...getRootProps()}
        className="w-[80%] dropzone px-4 py-2 flex flex-col items-center border-2 border-dashed border-black rounded-rd cursor-pointer text-center ml-2 mr-2 pt-6 pl-6 pb-6 pr-6 
        bg-gradient-to-b from-purple-600 to-purple-600 relative transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-300"
      >
        <input {...getInputProps()} />
        {/* Icon for uploading files */}
        <img
          className="w-20 mb-5 mt-5"
          src={add}
          alt="upload_file_icon"
          onClick={handleFileUpload}
        />
        {isDragActive ? (
          <div>
            {/* Displayed when files are being dragged */}
            <p className="pb-8 text-2xl font-Futura">Dropez vos fichiers ici...</p>
          </div>
        ) : (
          <div>
            {/* Displayed when no files are being dragged */}
            <p className="pb-8 text-2xl font-Futura">
              Déposez votre fichier ici ou<br /> parcourez pour le sélectionner
            </p>
          </div>
        )}
      </div>

      {/* Display selected files */}
      {files.length > 0 && (
        <div className="w-[80%] pl-5 mb-5 mt-5 font-Futura">
          {files.map((file, index) => (
            <div key={file.name} className=" mt-3 mb-3 flex items-center border-2 border-black rounded-rd bg-purple-600 relative duration-300 transform hover:bg-purple-300">
              {/* Display file icon on the left */}
              <div className="mr-6 pl-2  ">
                <FileIcon size={24} style={{ color: '#F6B237' }} />
              </div>

              {/* Display file information in the middle */}
              <div className="flex-grow ">
                <p className="text-left font-Futura pt-2 pb-2">{file.name} - {file.size} bytes </p>
              </div>

              {/* Display trash icon on the right */}
              <div onClick={() => removeFile(index)} className="cursor-pointer mr-5">
                <Trash2Icon size={24} style={{ color: '#F6B237' }} />
              </div>
            </div>
          ))}
          <div className="w-full flex justify-center mt-4">
            {/* Button to upload articles */}
            <button className="border-2 rounded-rd bg-blue2 text-center px-4 py-2" onClick={handleFileUpload}>
              Upload articles
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default FileUpload;
