import ListFavoriteArticles from "../components/ListFavoriteArticles";
import Displayer from "../components/Displayer";

const FavoriePage = () => {
   const userId = 1; // Replace with the actual authenticated user ID

   const results = [
     // ... sample article data ...
   ];

    return (
      <div
        className="relative w-full justify-center flex flex-col items-center h-[100vh] bg-cover bg-center relative"
        style={{
          backgroundImage: "url(../../../images/background.svg)",
        }}
      >
        <div className="text-black text-[3vw] z-20 font-Futura-bold mb-[60vh]">
          <p>Mes articles favoris</p>
        </div>
        div

      </div>
    );
    
  };


export default FavoriePage;