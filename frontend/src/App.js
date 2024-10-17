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
    if(newState === true){
      localStorage.setItem('loggedInStatus', newState);
    }else{
      localStorage.removeItem('loggedInStatus');
    }
  }

  const updateIsCreatingStatus = (newState) => {
    setIsCreatingAccount(newState);
  }

  useEffect(() => {
    const fecthLoginStatus = async () => {
      const loginStatusResponse = fetch('http://localhost/8000/get-logged-in-status', {
        method: 'GET',
        headers:{
          'Content-Type': 'application/json'
        }
      })

      const loginStatusResponseJson = await loginStatusResponse.json();
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
    };
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
