// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import DataPage from './pages/DataPage'; // Import the component for the new route
import './App.css'
import SearchResultPage from './pages/SearchResultPage';
const App = () => {
  return (
    <Router>
      <Routes>
        {/* Route for the SearchPage */}
        <Route path="/search" element={<SearchPage />} />

        {/* Route for the Home page */}
        <Route path="/" element={<DataPage />} />
        
        {/* Route for the SearchResultPage */}
        <Route path="/result" element={<SearchResultPage />} />
      </Routes>
    </Router>
  );
};

export default App;
