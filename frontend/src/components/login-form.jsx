import { useState } from "react";
import { clsx } from 'clsx';


function LoginForm({updateLoginStatus, updateIsCreatingStatus}){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();

        try{
            const response = await fetch('http://localhost:8000/sign-in', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    password
                })
            })
            
            if (!response.ok){
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Login Failed')
            }

            const responseData = await response.json();
            const access_token = responseData.AccessToken;
            localStorage.setItem('access_token', access_token);
            
            setMessage('');
            updateLoginStatus(true);
        }
        catch(error){
            setMessage(error.message)
        }
    }
    return(
        <div className= "flex items-center justify-center w-full h-screen">
             <form onSubmit = {handleLogin} className="mx-auto w-[350px] h-[440px] bg-gray-100 space-y-3 rounded-xl shadow-md">
                <div className = "h-[130px] w-full bg-green-700 rounded-t-xl text-white pl-6 pt-9">
                    <p className="font-semibold text-[1.8rem]">Sign In</p>
                    <p className = "">Please enter the credentials to log in.</p>
                </div>
                <div className = "w-full px-6">
                    <div className="mt-6">
                        <label htmlFor="Email" className="block mb-2">
                            Username
                        </label>
                        <input
                            type="text"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter your username"
                            onChange={(e) => {
                                setUsername(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className="mt-4">
                        <label htmlFor="password" className="block mb-2">
                            Password
                        </label>
                        <input
                            type="password"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter password"
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className = {clsx(
                        "text-red-500 mt-3 text-[0.9rem] opacity-0 h-[1.5rem]",
                        {
                            "opacity-100": message !== ''
                        },
                        )} 
                    >
                        <p>{message}</p>
                    </div>
                    <div className="mt-4 text-white">
                        <button type="submit" className="w-full h-[2rem] bg-green-700 ">Sign In</button>
                        <button onClick = {() => updateIsCreatingStatus(true)} className = "w-full h-[2rem] bg-green-700 mt-3">Create a new account</button>
                    </div>
                </div>
             </form>
        </div>
    )
}

export default LoginForm;