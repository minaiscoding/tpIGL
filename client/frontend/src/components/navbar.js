import React from 'react'
import logo from '../logo.svg';



export default function Navbar() {
    return ( 
        <div className=' bg-navBg'>
            <div className='flex justify-between h-[64px] flex-row items-center mx-4 bg-cover '>
                <div>
                    <img src={logo} alt='Logo' />
                </div>
                <div className='flex flex-row text-sm lg:text-lg  text-center gap-[32px]'>
                    <span></span>
                    <p className=' text-white text-sm sm:text-lg  font-Futura'>Rechercher</p>
                    <span></span>
                    <p className=' text-white text-sm sm:text-lg font-Futura'>Mes favoris</p>
                </div>
                <div className='flex flex-row text-center gap-[10px]'>
                    <span></span>
                    <p className=' text-white text-sm sm:text-lg font-Futura'>Mon Profile</p>
                </div>
            </div>
        </div>
    )
}
