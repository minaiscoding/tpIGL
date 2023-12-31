import React from 'react';
//import './Animation.css';
import a from '../../assets/a.png';
import r from '../../assets/r.png';
import t from '../../assets/t.png';
import i from '../../assets/i.png';
import c from '../../assets/c.png';
import l from '../../assets/l.png';
import o from '../../assets/o.png';

const letters = [a, r, t, i, c, l, o]; // Use imported images

function Animation() {
  return (
    <div className='animation-container'>
      {letters.map((letter, index) => (
        <img
          key={index}
          src={letter}
          className={`letter letter-${index} ${index === 0 ? 'visible' : ''}`}
          alt={`letter-${index}`}
        />
      ))}
    </div>
  );
}


export default Animation;
