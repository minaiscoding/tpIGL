import React, { useState } from 'react';
import axios from 'axios';
import logo from "../logo.svg";
import LoginImg from "../assets/login.png";

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error1, setError1] = useState('');
  const [error2, setError2] = useState('');
  const [error3, setError3] = useState('');


  const handleLogin = async () => {
    setError1("");
    setError2("");
    setError3("");

    if (username === "") {
      setError1("Vérifier votre nom d'utilisateur ");
    }
    if (email === "") {
      setError2("Vérifiez votre Email");
    }
    if (password === "") {
      setError3("Vérifier votre mot de passe ");
    }
    {/* else {
      try {
        const response = await axios.post(
          "API",
         { username, email, password }
        );
        const responseData = response.data;
        const token = responseData.data.member.memberId;
        Cookies.set("authToken", token, { expires: 7 }); // Set the cookie to expire in 7 days
        console.log("Sign-in successful", token);
        // window.location.href = "/my_account";
      } catch (error) {
        console.error("Error:", error);
        if (error.response) {
          console.error("Server Error Message:", error.response.data);
          setErrorMsg(error.response.data.message || "Sign-in failed");
        } else {
          setErrorMsg("An error occurred during sign-in");
        }
      }
    }*/}
  };

  return (
    <div className="sm:flex sm:flex-row flex flex-col items-center overflow-y-hidden">
      <div className="sm:w-[45%] sm:h-screen w-screen h-[30%] justify-between pt-[51px] sm:pt-[81px] s:rounded-tr-lg rounded-bl-lg rounded-br-lg flex flex-col items-center sm:bg-gradient-to-br  bg-gradient-to-b  from-f6b237 via-6b30e4 to-3635ce">
        <img src={logo} alt="Logo" className="sm:w-[50%]" />
        <img src={LoginImg} className="w-[60%] sm:h-[60%] h-[30%]" alt="Login Image" />
      </div>
      <div className="w-full sm:w-[55%] h-[70%] flex flex-col justify-center items-center">

        <form className="flex flex-col justify-center items-center align-middle gap-10 w-[75%] sm:w-[65%]">
          <h1 className="text-rgba-54-53-206-1 font-avantgarde text-center text-2xl sm:text-3xl font-extrabold mt-4"> Se Connecter </h1>

          <div className='w-full relative'>
            <input
              type="text"
              placeholder="Nom d'utilisateur"
              className={`border-[1.3px] border-solid border-rgba-54-53-206-1 rounded-md px-4 h-[46px] text-navBg text-base w-full ${error1 && 'border-yellow'}`}
              onChange={(e) => setUsername(e.target.value)}
            />
            {error1 && <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">{error1}</p>}
          </div>

          <div className='w-full relative'>
            <input
              type="email"
              placeholder="Email"
              className={`border-[1.3px] border-solid rounded-md  border-rgba-54-53-206-1 px-4 h-[46px] text-navBg text-base w-full ${error2 && 'border-yellow'}`}
              onChange={(e) => setEmail(e.target.value)}
            />
            {error2 && <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">{error2}</p>}
          </div>

          <div className='w-full relative'>
            <input
              type="password"
              placeholder="Mot de passe"
              className={`border-solid border-[1.3px] rounded-md px-4 h-[46px]  border-rgba-54-53-206-1 text-navBg text-base w-full ${error3 && 'border-yellow'}`}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error3 && <p className="text-yellow text-sm mt-2 absolute -bottom-5 left-2">{error3}</p>}
          </div>

          <button
            className="px-4 h-[55px] bg-rgba-54-53-206-1 w-full rounded-md text-[#fff] font-Futura text-center text-2xl"
            onClick={handleLogin}
          >
            Connecter
          </button>
        </form>

      </div>
    </div>
  );
};

export default LoginPage;
