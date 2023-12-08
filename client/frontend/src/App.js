import React from 'react';
import DataDisplay from './components/DataDisplay';

function App() {
  return (
    <div>
      <DataDisplay endpoint="utilisateurs" />
      <DataDisplay endpoint="articles" />
      <DataDisplay endpoint="favoris" />
    </div>
  );
}

export default App;