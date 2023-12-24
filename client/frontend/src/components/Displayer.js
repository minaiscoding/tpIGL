import React from 'react';

const Displayer = ({ children }) => {
  return (
    <div className="bg-white border border-black rounded-md p-4">
      {children}
    </div>
  );
};

export default Displayer;
