Derbal Rayhane
Derbal Rayhane#0305

Derbal Rayhane — 14/12/2023 17:23
Wow rani proud
Amina Chelli — 25/12/2023 16:57
Rayhane kolili asko nav f smal hadk wch habiti nti
Derbal Rayhane — 25/12/2023 16:58
mazerbtch att nzereb
Amina Chelli — 25/12/2023 16:58
Kifch??
Derbal Rayhane — 25/12/2023 16:59
3lh rani nhki b z
remplaci z b j hhhhhh
oui hkk amina n9si brk chwi space binathom
Amina Chelli — 25/12/2023 17:00
Derbal Rayhane — 25/12/2023 17:01
Amina mnich nsm3
Amina Chelli — 25/12/2023 17:02
Derbal Rayhane — 25/12/2023 17:05
Oui oui cnn mm haka rahi mliha
Amina Chelli — 01/01/2024 21:38
rayhane ad5li ma3lich
wla 9olili raki sur result.id ay tamchilk
???
Amina Chelli — Hier à 23:52
import React, { useEffect, useState } from "react";
import { Route, Routes, BrowserRouter as Router, useNavigate } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import DataPage from './pages/DataPage';
import Navbar from "./components/NavBar";
import LoginPage from './pages/LoginPage';
Afficher plus
App.js
5 Ko
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import logo from "../logo.svg";
import LoginImg from "../assets/login.png";
Afficher plus
LoginPage.js
6 Ko
﻿
Amina Chelli
amina3318
import React, { useEffect, useState } from "react";
import { Route, Routes, BrowserRouter as Router, useNavigate } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import DataPage from './pages/DataPage';
import Navbar from "./components/NavBar";
import LoginPage from './pages/LoginPage';
import AccueilPage from './pages/AccueilPage';
import UploadArticle from "./pages/UploadArticle";
import ListModerateurs from "./pages/ListModerateurs";
import DetailsArticle from "./pages/DetailsArticle";
import './App.css';
import FavoriePage from './pages/FavoriePage';
import SearchResultPage from './pages/SearchResultPage';
import { TextArticlePage } from "./pages/TextArticlePage";
import axios from "axios";


const CheckAuth = () => {
  const navigate = useNavigate();

  useEffect(() => {
    console.log()
    if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
      const checkAuthStatus = async () => {
        const isAuthenticated = localStorage.getItem('token');
        if (!isAuthenticated) {
          navigate("/");
        }
      };

      checkAuthStatus();
    }
  }, [navigate]);

  return null;
};

// Defining the App component
const App = () => {
  // State variables and constants
  const storedRole = localStorage.getItem("userRole");
  const [role, setRole] = useState(storedRole || "user");
  const [members, setMembers] = useState({});
  const [username, setUsername] = useState(localStorage.getItem('NomUtilisateurs'));

  const handleRoleChange = (newRole) => {
    setRole(newRole);

    localStorage.setItem("userRole", newRole);
  };



  const [loading, setLoading] = useState(false);
  useEffect(() => {
    // Set username based on localStorage after the component mounts
    const storedUsername = localStorage.getItem('NomUtilisateurs');
    if (storedUsername) {
      setUsername(storedUsername);
    }

    // Introduce a delay to simulate an asynchronous operation
    const delay = setTimeout(() => {
      setLoading(false); // Set loading to false after a delay (simulating async)
    }, 1000);

    // Clear the timeout to avoid memory leaks
    return () => clearTimeout(delay);
  }, []); // Empty dependency array ensures this runs once on mount


  return (

    <>
      {loading ? (
        "Loading ..."
      ) : (
        <div className=" relative h-full w-screen  min-h-screen">
          <Router>
            <Routes >
              <Route path="/" element={<AccueilPage />} />
              {/* Route for the LoginPage */}
              <Route path="/login" element={<LoginPage onRoleChange={handleRoleChange} />} />
              <Route
                path="/*"
                element={
                  <>
                    <CheckAuth />
                    <Navbar role={role} profile={username} />
                    <Routes>


                      {/* Route for the SearchPage */}
                      <Route path="/search" element={<SearchPage />} />

                      {/* Route for the DetailsPage */}
                      <Route path="/details/:articleId" element={<DetailsArticle role={role} />} />

                      {/* Route for the Home page */}
                      <Route path="/Data" element={<DataPage />} />

                      {/* Route for the text of the article page */}
                      <Route path="/TextIntegral/:articleId" element={< TextArticlePage />} />

                      {/* Route for the ModÃ©rateurPage */}
                      <Route path="/Moderateurs" element={<ListModerateurs />} />

                      {/* Route for the UplaodArticlePage */}
                      <Route path="/UploadArticle" element={<UploadArticle />} />

                      {/* Route for the SearchResultPage */}
                      <Route path="/result" element={<SearchResultPage />} />

                      {/* Route for the favorie page */}
                      <Route path="/mesFavoris" element={<FavoriePage />} />

                    </Routes>
                  </>
                }
              />
            </Routes>
          </Router>

        </div>
      )}
    </>
  );
}

export default App;