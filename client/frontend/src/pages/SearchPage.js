import React from 'react';

const SearchPage = () => {
  return (
    <div className="h-screen w-screen flex-col flex">
      {/* Background Image */}
      <div
        className="relative w-full justify-center flex flex-col items-center h-[57vh] bg-cover bg-center relative"
        style={{
          backgroundImage: 'url(../../../images/bgimg1.svg)',
        }}
      >
        {/* Overlay Pseudo-element */}
        <div className="absolute inset-0 bg-gradient-to-r from-purple-700 to-yellow-400 opacity-80 z-10"></div>

        {/* Content for the top half */}
        <div className="text-white font-bold text-5xl z-20 "> {/* Set font size to 5xl (40vw) */}
          <p>Découvrez l'excellence</p>
          <p>scientifique en un clic</p>
        </div>

        <div className="absolute translate-y-[18vh] h-[150vh] flex items-center justify-center z-20 w-[50vw]">
  <input
    type="text"
    placeholder="Search..."
    className="border border-r-0 border-gray-300 rounded-l-lg px-4 py-2 bg-white w-full"  
  />
  <button className="bg-gray-800 text-white px-[7%] py-2 rounded-r-lg">
    Search
  </button>
</div>

      </div>

      {/* Images Section */}
      <div className="w-1/2 flex items-center justify-around">
        {/* Replace these image URLs with your actual image paths */}
        <img className="w-1/3" src="/images/image1.jpg" alt="Product 1" />
        <img className="w-1/3" src="/images/image2.jpg" alt="Product 2" />
        <img className="w-1/3" src="/images/image3.jpg" alt="Product 3" />
      </div>
    </div>
  );
};

export default SearchPage;
