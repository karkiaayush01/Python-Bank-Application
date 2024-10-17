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
    localStorage.setItem('loggedInStatus', newState);
  }

  const updateIsCreatingStatus = (newState) => {
    setIsCreatingAccount(newState);
  }

  useEffect(() => {
    if(localStorage.getItem('loggedInStatus') == 'true'){
      setIsLoggedIn(true);
    }
  })
  

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