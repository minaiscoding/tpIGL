// AccueilPage.js
import Animation from '../components/Animation/Animation.js';
import ConnexionButton from '../components/ConnexionButton';

const AccueilPage = () => {
  const backgroundStyle = {
    backgroundImage: 'url(../../../images/bgimg1.svg)',
    // Add other background styles as needed
  };

  return (
    <div
      className="w-full justify-between sm:py-0 py-32 flex flex-col items-center h-[100vh] bg-cover bg-center relative"
      style={backgroundStyle}
    >
      <div className="absolute inset-0 bg-gradient-to-br justify-between py-4 flex flex-col items-center from-f6b2372 via-6b30e42 to-3635ce2 h-screen w-screen z-10">
        <h1 className='text-[#fff] font-avantgarde text-center text-4xl sm:text-6xl font-extrabold mt-4'>BIENVENU SUR</h1>
        <Animation backgroundStyle={backgroundStyle} />
        <ConnexionButton />
      </div>
    </div>
  );
};

export default AccueilPage;
