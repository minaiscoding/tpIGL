import React, { useState } from 'react';
import vector_bg from '../assets/Vector.svg';
import InfoArticle from '../components/InfoArticle';


// ADD HANDLE SUBLIT FOR THE BUTTON SAVE (INTEGRAION FCTN)
// ADD INTEGRATION FOR SUPPRIMER BUTTON 
// PiCK THE ROLE



const DetailsArticle = () => {
    const backgroundImage = `url(${vector_bg})`;
    const [edit, setEdit] = useState(false);
    const [role, setRole] = useState('modérateur');

    return (
        <div
            style={{ backgroundImage }}
            className='w-screen h-full min-h-screen  bg-purple-3OO bg-center bg-no-repeat flex flex-col items-center justify-center px-2 bg-cover pb-8 overflow-y-scroll'
        >


            <InfoArticle edit={edit} />

            {role === 'modérateur' ? (
                <div className='flex flex-row justify-center gap-4 md:gap-12 lg:gap-16 xl:gap-24'>
                    {!edit ? (
                        <>
                            <button
                                className='bg-white text-lg font-Futura text-navBg text-center rounded-sm px-6 md:px-12 py-2'
                                onClick={() => setEdit(true)}
                            >
                                Modifier
                            </button>
                            <button
                                className='bg-[#6B30E4] text-lg font-Futura text-white text-center rounded-sm px-6 md:px-12 py-2'
                            >
                                Supprimer
                            </button>
                        </>
                    ) : (
                        <>
                            <button
                                className='bg-[#6B30E4] text-lg font-Futura text-white text-center rounded-sm px-6 md:px-12 py-2'
                                onClick={() => setEdit(false)}
                            >
                                Enrigistrer
                            </button>
                            <button
                                className='bg-yellow text-lg font-Futura text-white text-center rounded-sm px-6 md:px-12 py-2'
                                onClick={() => setEdit(false)}
                            >
                                Annuler
                            </button>
                        </>
                    )}
                </div>
            ) : ''}
        </div>

    );
};

export default DetailsArticle;
