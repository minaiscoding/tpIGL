import React from 'react'
import { Link } from 'react-router-dom'

function ConnexionButton() {
  return (
    <Link to='/login'>
    <button className=' button-white font-Futura   '>
        Connexion
    </button>
    </Link>

  )
}

export default ConnexionButton