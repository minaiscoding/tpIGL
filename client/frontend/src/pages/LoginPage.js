import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import logo from "../logo.svg";
import LoginImg from "../assets/login.png";

const LoginPage = ({ onRoleChange }) => {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error1, setError1] = useState("");
  const [error2, setError2] = useState("");
  const [error3, setError3] = useState("");
  const [Erreutmsg, setErrorMsg] = useState("");

  const handleLogin = async () => {
    if (username === '') {
      setError1("Nom d'utilisateur ne doit pas etre vide")
    }
    else if (email === '') {
      setError2("Mot de passe ne doit pas etre vide")
    } else if (password === '') {
      setError3("Mot de passe  ne doit pas etre vide")
    }
    else {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/login/", {
          NomUtilisateur: username,
          MotDePasse: password,
          Email: email,
        });

        const responseData = response.data;
        const token = response.data.token; // Retrieve the token from the response data
        localStorage.setItem('token', token);
        localStorage.setItem("userRole", responseData.role);
        localStorage.setItem("NomUtilisateurs", responseData.utilisateur.NomUtilisateur);
        onRoleChange(responseData.role);

        localStorage.setItem('id', responseData.utilisateur.id);


        switch (responseData.role) {
          case "admin":
            window.location.href = "/UploadArticle";
            break;
          case "moderator":
            window.location.href = "/articles";
            break;
          case "user":

            window.location.href = "/search";
            break;
          default:
            break;
        }



      } catch (error) {
        console.error("Error:", error);
        if (error.response) {
          console.error("Server Error Message:", error.response.data);
          console.log("Server Error Message:", error.response.data);


          if (error.response.data.message === 'User not found') {
            setError1('vérifier votre nom d`utilisateur');
          }/* else if (error.response.data.field === "Email") {
          setError2(error.response.data.message || "Error in email");
        } */else if (error.response.data.message === 'Invalid password') {
            setError3('mot de passe incorrecte');
          } else {
            setErrorMsg(error.response.data.message || "Sign-in failed");
          }
        } else {
          setErrorMsg("An error occurred during sign-in");
        }
      }
    }



  };
  return (
    <div className="sm:flex sm:flex-row flex flex-col items-center overflow-y-hidden">
      <div className="sm:w-[45%] sm:h-screen w-screen h-[30%] justify-between pt-[51px] sm:pt-[81px] s:rounded-tr-lg rounded-bl-lg rounded-br-lg flex flex-col items-center sm:bg-gradient-to-br bg-gradient-to-b from-f6b237 via-6b30e4 to-3635ce">
        <img src={logo} alt="Logo" className="sm:w-[50%]" />
        <img
          src={LoginImg}
          className="w-[60%] sm:h-[60%] h-[30%]"
          alt="Login Image"
        />
      </div>
      <div className="w-full sm:w-[55%] h-[70%] flex flex-col justify-center items-center">
        <form className="flex flex-col justify-center items-center align-middle gap-10 w-[75%] sm:w-[65%]"
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
        >
          <h1 className="text-rgba-54-53-206-1 font-avantgarde text-center text-2xl sm:text-3xl font-extrabold mt-4">
            {" "}
            Se Connecter{" "}
          </h1>

          <div className="w-full relative">
            <input
              type="text"
              placeholder="Nom d'utilisateur"
              className={`border-[1.3px] border-solid border-rgba-54-53-206-1 rounded-md px-4 h-[46px] text-navBg text-base w-full ${error1 && "border-yellow"
                }`}
              onChange={(e) => setUsername(e.target.value)}
            />
            {error1 && (
              <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">
                {error1}
              </p>
            )}
          </div>

          <div className="w-full relative">
            <input
              type="email"
              placeholder="Email"
              className={`border-[1.3px] border-solid rounded-md border-rgba-54-53-206-1 px-4 h-[46px] text-navBg text-base w-full ${error2 && "border-yellow"
                }`}
              onChange={(e) => setEmail(e.target.value)}
            />
            {error2 && (
              <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">
                {error2}
              </p>
            )}
          </div>

          <div className="w-full relative">
            <input
              type="password"
              placeholder="Mot de passe"
              className={`border-solid border-[1.3px] rounded-md px-4 h-[46px]  border-rgba-54-53-206-1 text-navBg text-base w-full ${error3 && "border-yellow"
                }`}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error3 && (
              <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">
                {error3}
              </p>
            )}
          </div>

          <button
            className="px-4 h-[55px] bg-rgba-54-53-206-1 w-full rounded-md text-[#fff] font-Futura text-center text-2xl"
            type="submit"
          >
            Connecter
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
