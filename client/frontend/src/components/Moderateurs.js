import React from 'react';
import Moderateur from './Moderateur';


function Moderateurs(moderateurs) {
    return (
        <div>
            {moderateurs.map((moderateur)=>(
                <Moderateur moderateur={moderateur} />
            ))}
        </div>
    );
}

export default Moderateurs;