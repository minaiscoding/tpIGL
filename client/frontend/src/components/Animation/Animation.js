import React from 'react';
import './Animation.css';
import logo from '../../logo.svg';

function Animation() {
  return (
    <div className='animation-container w-[80%] '>
      <img src={logo} className='w-full' alt='Logo' />
    </div>
  );
}

export default Animation;
