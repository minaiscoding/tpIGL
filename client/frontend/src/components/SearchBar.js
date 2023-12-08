import React, { useState } from 'react';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`/api/search/?q=${query}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error performing search:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      <div>
        <h2>Search Results</h2>
        <ul>
          {searchResults.map((result, index) => (
            <li key={index}>
              <strong>Title:</strong> {result.Titre},{' '}
              <strong>Summary:</strong> {result.Resume},{' '}
              <strong>Authors:</strong> {result.auteurs},{' '}
              <strong>Institution:</strong> {result.Institution}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SearchBar;
