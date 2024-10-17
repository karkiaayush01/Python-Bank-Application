import SideNav from "./sidenav";
import Deposit from "./deposit";
import Withdraw from "./withdraw";
import Overview from "./overview";
import { useState, useEffect } from "react";

function BankApp({updateLoginStatus}){
    const[currentUser, setCurrentUser] = useState(null);
    const[activePage, setActivePage] = useState('overview')

    const updateActivePage = (newState) => {
        setActivePage(newState)
    }
    
    useEffect(() => {
        const fetchUserData = async () => {
            try{
                const userResponse = await fetch('http://localhost:8000/get-user-data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })

                const responseData = await userResponse.json();
                setCurrentUser(responseData);
            }
            catch(error){
                console.log("Failed to fetch user data.");
            }
        };

        fetchUserData();
    }, []);

    if(!currentUser){
        return(
            <div>Loading...</div>
        )
    }

    return(
        <div className="w-full h-screen flex">
            <SideNav updateActivePage = {updateActivePage} username = {currentUser.username} updateLoginStatus={updateLoginStatus}/>
            {activePage === 'overview' ? <Overview /> :
                activePage === 'deposit' ?  <Deposit /> :
                <Withdraw />
            }
        </div>
    )
}

export default BankApp;