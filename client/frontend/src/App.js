import React, { useEffect, useState } from "react";
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import DataPage from './pages/DataPage';
import Navbar from './components/navbar';
import LoginPage from './pages/LoginPage';
import AccueilPage from './pages/AccueilPage'
import UploadArticle from "./pages/UploadArticle";
import ListModerateurs from "./pages/ListModerateurs";
import DetailsArticle from "./pages/DetailsArticle";
import './App.css';
import Favoris from "./pages/Favoris";



const App = () => {
  const [loading, setLoading] = useState(false);
  return (

    <>
      {loading ? (
        "Loading"
      ) : (
        <div className=" relative h-full w-screen  min-h-screen">
          <Router>
            <Routes>
              <Route path="/" element={<AccueilPage />} />
              {/* Route for the LoginPage */}
              <Route path="/login" element={<LoginPage />} />
              <Route
                path="/*"
                element={
                  <>
                    <Navbar />
                    <Routes>
                      

                      {/* Route for the SearchPage */}
                      <Route path="/search" element={<SearchPage />} />

                      {/* Route for the DetailsPage */}
                      <Route path="/details" element={<DetailsArticle />} />

                      {/* Route for the Home page */}
                      <Route path="/Data" element={<DataPage />} />

                      {/* Route for the favoris page */}
                      <Route path="/mesFavoris" element={<Favoris />} />

                      {/* Route for the ModérateurPage */}
                      <Route path="/Moderateurs" element={<ListModerateurs />} />

                      {/* Route for the UplaodArticlePage */}
                      <Route path="/UploadArticle" element={<UploadArticle />} />

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
