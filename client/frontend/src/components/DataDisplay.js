import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DataDisplay = ({ endpoint }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/${endpoint}/`)
      .then(response => setData(response.data))
      .catch(error => console.error('Error fetching data:', error));
  }, [endpoint]);

  return (
    <div>
      <h2>{endpoint.charAt(0).toUpperCase() + endpoint.slice(1)} Data</h2>
      <ul>
        {data.map(item => (
          <li key={item.id}>{JSON.stringify(item)}</li>
        ))}
      </ul>
    </div>
  );
};

export default DataDisplay;
