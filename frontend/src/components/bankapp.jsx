import SideNav from "./sidenav";
import Deposit from "./deposit";
import Withdraw from "./withdraw";
import Overview from "./overview";
import { useState, useEffect } from "react";
import LoadingPage from "./loading";

function BankApp({updateLoginStatus}){
    const[activePage, setActivePage] = useState('overview');
    const[userData, setUserData] = useState(null);
    const[username, setUserName] = useState('');

    const updateActivePage = (newState) => {
        setActivePage(newState)
    }

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const fetchUserData = async () => {
            try{
                const response = await fetch('http://localhost:8000/get-user-data', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if(response.ok){
                    const responseJson = await response.json();
                    setUserData(responseJson);
                    setUserName(responseJson.username);
                }
                else{
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "An error occured");
                }
            }
            catch(err){
                console.error(err.message);
            }
        }

        fetchUserData();
    }, []);


    return(
        <div className="w-full h-screen flex">
            <SideNav updateActivePage = {updateActivePage} username = {username} updateLoginStatus={updateLoginStatus}/>
            {activePage === 'overview' ? (
                userData ? (
                    <Overview userData = {userData} /> 
                ) : (
                    <LoadingPage />
                )
            ): activePage === 'deposit' ? ( 
                <Deposit /> 
            ) : (
                <Withdraw />
            )
            }
        </div>
    )
}

export default BankApp;