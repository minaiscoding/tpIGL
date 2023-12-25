import React from "react";

const NavBar = () => {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto">
        <div className="flex items-center justify-between">
          <div className="text-white font-bold text-xl">Your Logo</div>
          <div className="flex items-center space-x-4">
            <a href="#" className="text-white">
              Home
            </a>
            <a href="#" className="text-white">
              About
            </a>
            <a href="#" className="text-white">
              Contact
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
