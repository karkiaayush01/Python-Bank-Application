import logo from './logo.svg';
import './App.css';
import LoginForm from './components/login-form';
import CreateForm from './components/create-form';
import BankApp from './components/bankapp';
import { useState, useEffect } from 'react';
import LoadingPage from './components/loading';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const updateLoginStatus = (newState) => {
    setIsLoggedIn(newState);
  }

  const updateIsCreatingStatus = (newState) => {
    setIsCreatingAccount(newState);
  }

  useEffect(() => {
    const checkSession = async () => {
      if (localStorage.getItem('access_token')){
        try{
          const token = localStorage.getItem('access_token')
          const response = await fetch('http://localhost:8000/validate-token', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
    
          if (response.ok){
            updateLoginStatus(true);
          }
          else{
            const errorData = await response.json();
            console.error('Error response:', errorData);
            localStorage.removeItem('access_token');
            updateLoginStatus(false)
          }
        }
        catch(err){
          localStorage.removeItem('access_token')
          updateLoginStatus(false);
          console.error("Session validation failed", err)
        }
      }
      else{
        updateLoginStatus(false);
      }
    }

    checkSession()
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
