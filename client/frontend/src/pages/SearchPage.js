import React from 'react';


const SearchPage = () => {
  return (
    <div className="h-full w-screen flex-col  items-center flex font-Futura">
      {/* Background Image */}
      <div
        className=" w-full justify-center flex flex-col items-center h-[57vh] bg-cover bg-center relative"
        style={{
          backgroundImage: 'url(../../../images/bgimg1.svg)',
        }}
      >
        {/* Overlay Pseudo-element */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#3635CE] to-[#F6B237] opacity-80 z-10"></div>

        {/* Content for the top half */}
        <div className="text-white text-[3vw] z-20 font-Futura-bold mb-[7vh]">
  <p>Découvrez l'excellence</p>
  <p>scientifique en un clic</p>
</div>


<div className="absolute translate-y-[18vh] h-[200px] flex items-center justify-center z-20 w-[50vw]">
  <input
    type="text"
    placeholder="Rechercher un article"
    className="border border-r-0 border-gray-300 rounded-l-md px-4 py-3 bg-white w-full"  
  />
  <button className="bg-gray-800 text-white px-[6%] py-3 rounded-r-md">
    Search
  </button>
</div>

      </div>

{/* Bottom Section */}
<div className="flex flex-col items-center justify-center gap-2 h-full py-[2%] w-full">
 {/* Lines next to the text */}
<div className="flex items-center gap-4">
<svg xmlns="http://www.w3.org/2000/svg" width="411" height="6" viewBox="0 0 411 6" fill="none">
  <path opacity="0.5" d="M0.333333 3C0.333333 4.47276 1.52724 5.66667 3 5.66667C4.47276 5.66667 5.66667 4.47276 5.66667 3C5.66667 1.52724 4.47276 0.333333 3 0.333333C1.52724 0.333333 0.333333 1.52724 0.333333 3ZM405.347 3C405.347 4.47276 406.541 5.66667 408.013 5.66667C409.486 5.66667 410.68 4.47276 410.68 3C410.68 1.52724 409.486 0.333333 408.013 0.333333C406.541 0.333333 405.347 1.52724 405.347 3ZM3 3.5H408.013V2.5H3V3.5Z" fill="#1E1E1E"/>
</svg>
  <p className="text-center text-2xl font-bold mb-4">
    Que pouvez-vous faire avec <span className="font-Futura-bold text-[#3635CE]">articlo</span>
  </p>
  <svg xmlns="http://www.w3.org/2000/svg" width="411" height="6" viewBox="0 0 411 6" fill="none">
  <path opacity="0.5" d="M0.333333 3C0.333333 4.47276 1.52724 5.66667 3 5.66667C4.47276 5.66667 5.66667 4.47276 5.66667 3C5.66667 1.52724 4.47276 0.333333 3 0.333333C1.52724 0.333333 0.333333 1.52724 0.333333 3ZM405.347 3C405.347 4.47276 406.541 5.66667 408.013 5.66667C409.486 5.66667 410.68 4.47276 410.68 3C410.68 1.52724 409.486 0.333333 408.013 0.333333C406.541 0.333333 405.347 1.52724 405.347 3ZM3 3.5H408.013V2.5H3V3.5Z" fill="#1E1E1E"/>
</svg>
</div>


  {/* Images Section */}
<div className="grid grid-cols-3 gap-20 items-center justify-center h-full">
  {/* Replace these image URLs with your actual image paths */}
  <img className="w-[80%] h-[80%] object-cover items-center mx-auto" src="../../../images/offer2.svg" alt="Product 1" />
  <img className="w-full h-full object-cover items-center" src="../../../images/offer1.svg" alt="Product 2" />
  <img className="w-[80%] h-[80%] object-cover items-center mx-auto" src="../../../images/offer3.svg" alt="Product 3" />
</div>

</div>




    </div>
  );
};

export default SearchPage;
