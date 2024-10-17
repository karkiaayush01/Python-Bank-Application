import logo from './logo.svg';
import './App.css';
import LoginForm from './components/login-form';
import CreateForm from './components/create-form';
import BankApp from './components/bankapp';
import { useState, useEffect } from 'react';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);

  const updateLoginStatus = (newState) => {
    setIsLoggedIn(newState);
    localStorage.setItem('loggedInStatus', String(newState));
  }

  const updateIsCreatingStatus = (newState) => {
    setIsCreatingAccount(newState);
  }

  useEffect(() => {
    const fecthLoginStatus = async () => {
      try{
        const loginStatusResponse = await fetch('http://localhost:8000/get-logged-in-status', {
          method: 'GET',
          headers:{
            'Content-Type': 'application/json'
          }
        })
  
        const loginStatusResponseJson = await loginStatusResponse.json();
        console.log(loginStatusResponseJson);
        if (loginStatusResponseJson.message === 'true'){
          if(localStorage.getItem('loggedInStatus') === 'true'){
            updateLoginStatus(true);
          }
          else{
            updateLoginStatus(false);
          }
        }
        else{
          updateLoginStatus(false);
        }
      }
      catch(error){
        console.log(error.message);
        updateLoginStatus(false);
      }
    };

    fecthLoginStatus();
  }, [])
  

  return (
    <div className="w-full h-full">
      {isLoggedIn ? (
        <BankApp updateLoginStatus = {updateLoginStatus}/>
      ) : (
        isCreatingAccount ? (
          <CreateForm updateIsCreatingStatus = {updateIsCreatingStatus}/>
        ): 
        <LoginForm 
          updateLoginStatus={updateLoginStatus} 
          updateIsCreatingStatus = {updateIsCreatingStatus}
        />
    )}
    </div>
  );
}

export default App;
