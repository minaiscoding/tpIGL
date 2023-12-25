import React, { useState, useEffect } from 'react';
import { FiSearch } from 'react-icons/fi';
import { LuFileText } from 'react-icons/lu';
import { Link, useLocation } from 'react-router-dom';
import logo from '../logo.svg';
import { FaAngleDown, FaAngleUp } from 'react-icons/fa6';
import { TfiWidgetized } from "react-icons/tfi";
import { IoIosLogOut } from 'react-icons/io';
import { SlMenu } from 'react-icons/sl';
import { CgClose } from "react-icons/cg";
import line from "../assets/Line.png";

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
                                className={`relative  -right-5 top-1 ${activeClassName === '/search' ? 'text-yellow' : 'text-[#fff]'}`}
                            />
                            <Link to="/search" onClick={() => changeActiveClassName('/search')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/search' ? 'text-yellow' : 'text-[#fff]'}`}
                                >
                                    Rechercher
                                </p>
                            </Link>
                            <LuFileText
                                className={`relative  -right-5 top-1 ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-[#fff]'}`}
                            />
                            <Link to="/mesFavoris" onClick={() => changeActiveClassName('/mesFavoris')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/mesFavoris' ? 'text-yellow' : 'text-[#fff]'}`}
                                >
                                    Mes Favoris
                                </p>
                            </Link>
                        </>
                    ) : role === 'admin' ? (
                        <>
                            <LuFileText
                                className={`relative  -right-5 top-1 ${activeClassName === '/UploadArticle' ? 'text-yellow' : 'text-[#fff]'}`}
                            />
                            <Link to="/UploadArticle" onClick={() => changeActiveClassName('/UploadArticle')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/UploadArticle' ? 'text-yellow' : 'text-[#fff]'}`}
                                >
                                    Uplaod Article
                                </p>
                            </Link>
                            <TfiWidgetized
                                className={`relative  -right-5 top-1 ${activeClassName === '/Moderateurs' ? 'text-yellow' : 'text-[#fff]'}`}
                            />
                            <Link to="/Moderateurs" onClick={() => changeActiveClassName('/Moderateurs')}>
                                <p
                                    className={` font-Futura ${activeClassName === '/Moderateurs' ? 'text-yellow' : 'text-[#fff]'}`}
                                >
                                    Modérateurs
                                </p>
                            </Link>
                        </>
                    ) : null}
                </div>
                <div className="flex relative flex-row text-center gap-[10px] items-center">
                    <div className="w-[36px] h-[36px] rounded-full overflow-hidden">
                        <img className="w-full h-full object-cover bg-[#fff]" alt="" />
                    </div>
                    <div className=" flex flex-row items-center justify-center gap-1 mr-4">
                        <p className="text-[#fff] font-Futura">Mon Profile</p>
                        <div className="flex flex-col">
                            {deconect ? (
                                <FaAngleUp className="text-[#fff] cursor-pointer top-1 relative" onClick={() => setDeconect(false)} />
                            ) : (
                                <FaAngleDown className="text-[#fff] cursor-pointer  top-1 relative" onClick={() => setDeconect(true)} />
                            )}
                            {deconect && (
                                <div className=" absolute top-10 right-4 z-50">
                                    <button className=' text-navBg flex gap-2 justify-center text-lg font-Futura text-center bg-[#fff] rounded-sm mt-1 px-4 py-2 shadow-navBg'>
                                        <IoIosLogOut className='relative   top-1 ' />
                                        Déconnecter
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </div>
            <div className="sm:hidden">
                <SlMenu
                    className="absolute top-4 right-8 text-2xl text-[#fff] z-50 font-bold cursor-pointer"
                    onClick={() => setShownav(!shownav)} // Toggle the state on click
                />
                {shownav && (
                    <div className='relative'>

                        <div
                            className="fixed inset-0 bg-[#000] opacity-20 z-50 text-Futura h-screen w-screen"
                            onClick={() => setShownav(false)}
                        ></div>
                        <div className="absolute w-1/2 flex flex-col right-0 top-0 h-screen z-50 bg-[#fff] items-center text-lg  align-middle ">

                            <CgClose className=' absolute top-1 right-6 text-[#ffff] z-50 cursor-pointer' onClick={() => setShownav(false)} />
                            <div className='flex flex-row gap-4 items-center justify-center  pb-3  pt-6 bg-yellow w-full '>
                                <div className="w-[36px] h-[36px] rounded-full overflow-hidden bg-[#ffff]">
                                    <img className="w-full h-full object-cover" alt="" />
                                </div>
                                <p>Amina </p>
                            </div>
                            <img src={line} />

                            {role === 'user' ? (
                                <>
                                    <div className={`flex flex-row gap-2  py-6 w-full justify-center items-center`} >

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
                                    <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center  `} >

                                        <LuFileText
                                            className={` text-navBg `}
                                        />
                                        <Link to="/search" onClick={() => changeActiveClassName('/search')}>
                                            <p
                                                className={` font-Futura text-navBg`}
                                            >
                                                Uplaod Article
                                            </p>
                                        </Link>
                                    </div>
                                    <img src={line} />

                                    <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center `} >

                                        <TfiWidgetized
                                            className={` text-navBg `}
                                        />
                                        <Link to="/mesFavoris" onClick={() => changeActiveClassName('/mesFavoris')}>
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
                            <div className={`flex flex-row gap-2 items-center py-6 w-full justify-center  cursor-pointer`} >

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