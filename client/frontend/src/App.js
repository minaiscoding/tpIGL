import React, { useEffect, useState } from "react";
import { Route, Routes, BrowserRouter as Router, useNavigate } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import DataPage from "./pages/DataPage";
import Navbar from "./components/NavBar";
import LoginPage from "./pages/LoginPage";
import AccueilPage from "./pages/AccueilPage";;
import UploadArticle from "./pages/UploadArticle";
import ListModerateurs from "./pages/ListModerateurs";
import DetailsArticle from "./pages/DetailsArticle";
import './App.css';
import FavoriePage from './pages/FavoriePage';
import SearchResultPage from './pages/SearchResultPage';
import AllArticles from "./pages/AllArticles";



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
                      {/* Route for the articles page */}
                      <Route path="/articles" element={<AllArticles />} />


                      {/* Route for the ModérateurPage */}
                      <Route
                        path="/Moderateurs"
                        element={<ListModerateurs />}
                      />


                      {/* Route for the UplaodArticlePage */}
                      {/*<Route path="/UploadArticle" element={<UploadArticle />} />*/}
                      <Route
                        path="/UploadArticle"
                        element={<UploadArticle />}
                      />

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
};

export default App;
