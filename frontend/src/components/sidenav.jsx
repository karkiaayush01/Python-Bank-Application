import { BanknotesIcon, BuildingOffice2Icon, HomeIcon, CreditCardIcon, UserCircleIcon, PowerIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';
import { useState, useEffect } from 'react';

function SideNav({updateActivePage, username, updateLoginStatus}){
    const [active, setActive] = useState('overview');
    const [userMenuActive, setUserMenuActive] = useState(false);
    const [shouldLogout, setShouldLogout] = useState(false);

    function toggleUserMenu(){
        setUserMenuActive(!userMenuActive);
    }

    useEffect(() => {
        if (shouldLogout) {
            const fetchLogout = async () => {
                try{
                    const logoutResponse = await fetch('http://localhost:8000/user-logout',{
                        method: 'POST',
                        'Content-Type': 'application/json'
                    })

                    if (!logoutResponse.ok){
                        throw new Error("An error occured.")
                    }
                }
                catch(error){
                    console.log("error.message")
                }
            };
            fetchLogout();
            setShouldLogout(false);
            updateLoginStatus(false);
            
        }
    }, [shouldLogout]);


    return(
        <div className="md:w-[230px] md:block hidden h-screen bg-gray-100 shadow-lg p-4 font-[Poppins] text-green-700 flex-shrink-0">
            <div className='flex text-green-700 mt-5 h-[6%]'>
                <BuildingOffice2Icon className='size-10' /> 
                <p className='mt-3.5 ml-1 font-[700]'>PyBank</p>
            </div>
            <div className='flex flex-col w-full mt-8 h-[75%] text-[0.9rem] gap-3'>
                <button className={clsx(
                    'w-full h-[45px] bg-white text-left flex items-center pl-4 rounded-lg',
                    {'!text-white !bg-green-700' : active === 'overview'},
                    'hover:bg-green-700 hover:text-white'
                    )} 
                    onClick={() => {
                        setActive('overview');
                        updateActivePage('overview');
                    }}  
                >
                    <HomeIcon className='size-6 mr-2' />
                    <p>Overview</p>
                </button>
                <button className= {clsx(
                    'w-full h-[45px] bg-white text-left flex items-center pl-4 rounded-lg hover:bg-green-700 hover:text-white',
                    {'!text-white !bg-green-700' : active === 'deposit'}
                    )}
                    onClick={() => {
                        setActive('deposit');
                        updateActivePage('deposit');
                    }}  
                >
                    <BanknotesIcon className='size-6 mr-2' />
                    <p>Deposit</p>
                </button>
                <button className= {clsx(
                    'w-full h-[45px] bg-white text-left flex items-center pl-4 rounded-lg hover:bg-green-700 hover:text-white',
                    {'!text-white !bg-green-700' : active === 'withdraw'}
                    )}
                    onClick={() => {
                        setActive('withdraw');
                        updateActivePage('withdraw');
                    }}  
                >
                    <CreditCardIcon className='size-6 mr-2' />
                    <p>Withdraw</p>
                </button>
            </div>
            <div className='w-full h-[10%] mt-3 relative'>
                <div className={clsx(
                        'absolute h-[80px] bg-white rounded-lg w-full top-[-85px] flex flex-col transition-all duration-300 ease-in-out z-0',
                        userMenuActive? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0 pointer-events-none'
                    )}
                >
                    <button className=
                        'w-full h-[50%] flex items-center pl-4 text-red-500 hover:bg-red-500 hover:text-white rounded-lg' 
                        onClick = {() => setShouldLogout(true)}          
                    >
                        <PowerIcon className='size-5 mr-2'/>
                        <p>Sign Out</p>
                    </button>
                </div>
                <button className= {clsx(
                    'w-full h-[45px] bg-white text-left flex items-center pl-4 rounded-lg hover:bg-green-700 hover:text-white z-100',
                    )}
                    onClick={toggleUserMenu}
                >
                    <UserCircleIcon className='size-6 mr-2' />
                    <p>{username}</p>
                </button>
            </div>
        </div>
    )
}

export default SideNav;