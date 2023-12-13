

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import DataPage from './pages/DataPage'; // Import the component for the new route
import Navbar from './components/navbar';
import './App.css'
const App = () => {
  return (
    <div>
      <Navbar />
      <Router>
        <Routes>
          {/* Route for the SearchPage */}
          <Route path="/search" element={<SearchPage />} />

          {/* Route for the Home page */}
          <Route path="/" element={<DataPage />} />

          {/* Add more routes as needed */}
        </Routes>
      </Router>
    </div>
  );
};

export default App;