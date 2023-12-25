import React, { useState, useEffect } from 'react';
import { FiSearch } from 'react-icons/fi';
import { LuFileText } from 'react-icons/lu';
import { SiWindows11 } from "react-icons/si";
import { Link, useLocation } from 'react-router-dom';
import logo from '../logo.svg';
import { FaAngleDown, FaAngleUp } from 'react-icons/fa6';
import { IoIosLogOut } from 'react-icons/io';
import { SlMenu } from 'react-icons/sl';
import { IoCloseOutline } from "react-icons/io5";
import line from "../assets/Line_nav.svg"
import FavorisIcon from './FavorisIcon';

export default function Navbar() {
    const [role, setRole] = useState('user');
    const [deconect, setDeconect] = useState(false);
    const location = useLocation();
    const [shownav, setShownav] = useState(false);
    const [activeClassName, setActiveClassName] = useState('');

    useEffect(() => {
        // Update active class when the location changes
        const pathname = location.pathname;
        setActiveClassName(pathname);
        setShownav(false);
    }, [location]);

    function changeActiveClassName(name) {
        setActiveClassName(name);
    }

    return (
        <div>
            <div className="hidden sm:flex sm:bg-navBg sm:w-screen sm:font-medium sm:justify-between sm:h-[64px] sm:flex-row sm:items-center px-4 sm:text-md md:text-lg">
                <div>
                    <img src={logo} alt="Logo" />
                </div>
                <div className="flex flex-row text-center gap-6">
                    {role === 'user' ? (
                        <>

                            <FiSearch
                                className={`relative  -right-5 top-1 ${activeClassName === '/search' ? 'text-yellow' : 'text-white'}`}
                            />
                            <Link to="/search" onClick={() => changeActiveClassName('/search')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/search' ? 'text-yellow' : 'text-white'}`}
                                >
                                    Rechercher
                                </p>
                            </Link>
                            <LuFileText
                                className={`relative  -right-5 top-1 ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-white'}`}
                            />
                            <Link to="/mesFavoris" onClick={() => changeActiveClassName('/mesFavoris')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-white'}`}
                                >
                                    Mes Favoris
                                </p>
                            </Link>
                        </>
                    ) : role === 'admin' ? (
                        <>
                            <LuFileText
                                className={`relative  -right-5 top-1 ${activeClassName === '/search' ? 'text-yellow' : 'text-white'}`}
                            />
                            <Link to="/search" onClick={() => changeActiveClassName('/search')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/search' ? 'text-yellow' : 'text-white'}`}
                                >
                                    Uplaod Article
                                </p>
                            </Link>
                            <SiWindows11
                                className={`relative  -right-5 top-1 ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-white'}`}
                            />
                            <Link to="/mesFavoris" onClick={() => changeActiveClassName('/mesFavoris')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-white'}`}
                                >
                                    Modérateurs
                                </p>
                            </Link>
                        </>
                    ) : null}
                </div>
                <div className="flex flex-row text-center gap-[10px] items-center">
                    <div className="w-[36px] h-[36px] rounded-full overflow-hidden">
                        <img className="w-full h-full object-cover bg-white" alt="" />
                    </div>
                    <div className="flex flex-row items-center justify-center gap-1 mr-4">
                        <p className="text-white font-Futura">Mon Profile</p>
                        <div className="flex flex-col">
                            {deconect ? (
                                <FaAngleUp className="text-white cursor-pointer top-1 relative" onClick={() => setDeconect(false)} />
                            ) : (
                                <FaAngleDown className="text-white cursor-pointer  top-1 relative" onClick={() => setDeconect(true)} />
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="sm:hidden">
                <SlMenu
                    className="absolute top-4 right-8 text-2xl text-white z-50 font-bold"
                    onClick={() => setShownav(!shownav)} // Toggle the state on click
                />
                {shownav && (
                    <div>
                        <div
                            className="fixed inset-0 bg-black opacity-20 z-50 text-Futura h-screen w-screen"
                            onClick={() => setShownav(false)}
                        ></div>
                        <div className="absolute w-1/2 flex flex-col right-0 top-0 h-screen z-50 bg-white items-center  align-middle ">

                            <div className=' relative flex flex-row gap-4  items-center py-6 w-full  justify-center bg-yellow'>
                                <IoCloseOutline className='text-white absolute top-2 right-4 cursor-pointer mb-4' size="24" onClick={() => setShownav(false)} />
                                <div className="w-[36px] h-[36px] rounded-full overflow-hidden bg-white">
                                    <img className="w-full h-full object-cover" alt="" />
                                </div>
                                <p>Mon profile</p>
                            </div>
                            <img scr={line} />

                            {role === 'user' ? (
                                <>
                                    <div className={`flex flex-row gap-2  py-6 w-full justify-center items-center `} >

                                        <FiSearch
                                            className={` text-navBg `}
                                        />
                                        <Link to="/search" onClick={() => changeActiveClassName('/search')}>
                                            <p
                                                className={` font-Futura text-navBg `}
                                            >
                                                Rechercher
                                            </p>
                                        </Link>
                                    </div>
                                    <img src={line} />
                                    <div className={`flex flex-row gap-2 py-6 w-full justify-center  items-center`} >
                                        <LuFileText
                                            className={`text-navBg `}
                                        />
                                        <Link to="/mesFavoris" onClick={() => changeActiveClassName('/mesFavoris')}>
                                            <p
                                                className={` font-Futura text-navBg`}
                                            >
                                                Mes favoris
                                            </p>
                                        </Link>
                                    </div>
                                    <img src={line} />

                                </>
                            ) : role === 'admin' ? (
                                <>
                                    <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center`} >

                                        <FiSearch
                                            className={` text-navBg `}
                                        />
                                        <Link to="/UploadArticle" onClick={() => changeActiveClassName('/UploadArticle')}>
                                            <p
                                                className={` font-Futura text-navBg`}
                                            >
                                                Uplaod Article
                                            </p>
                                        </Link>
                                    </div>
                                    <img src={line} />

                                    <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center  `} >

                                        <LuFileText
                                            className={` text-navBg `}
                                        />
                                        <Link to="/ListeModerateurs" onClick={() => changeActiveClassName('/Moderateurs')}>
                                            <p
                                                className={` font-Futura text-navBg `}
                                            >
                                                Modérateurs
                                            </p>
                                        </Link>
                                    </div>
                                    <img src={line} />

                                </>
                            ) : null}
                            <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center `} >

                                <IoIosLogOut
                                    className={` text-navBg `}
                                />
                                <p
                                    className={` font-Futura text-navBg `}
                                >
                                    Déconnecter
                                </p>
                            </div>
                        </div>

                        <div>

                        </div>

                    </div>
                )}
            </div>

        </div >
    );
}
