import { useState } from "react";
import { clsx } from "clsx";

import ConfirmationPage from "./confirmation";

function CreateForm({updateIsCreatingStatus}){
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [balance, setBalance] = useState('');
    const [message, setMessage] = useState('');
    const [confirmationPage, setConfirmationPage] = useState(false);

    const updateConfirmationStatus = (value) => {
        setConfirmationPage(value);
    }

    const handleSubmit = async (e) => {
        e.preventDefault(); 

        try{
            if (balance === ''){
                throw new Error('Empty Fields Found.')
            }
            else if (isNaN(Number(balance))){
                throw new Error('Invalid balance amount.')
            }

            const response = await fetch('http://localhost:8000/sign-up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    email,
                    password,
                    balance
                }),
            });
            
            if (!response.ok){
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login Failed');
            }

            const data = await response.json();
            setMessage(data.message);
            
            updateConfirmationStatus(true);
            e.target.elements.usernameField.value = '';
            e.target.elements.emailField.value = '';
            e.target.elements.passwordField.value = '';
            e.target.elements.balanceField.value = '';

        }
        catch(error){
            setMessage(error.message);
        }
    }

    return confirmationPage ? (
        <ConfirmationPage updateConfirmationStatus = {updateConfirmationStatus} updateIsCreatingStatus = {updateIsCreatingStatus} username = {username}/>   
    ) : (
        <div className= "flex items-center justify-center w-full h-screen">
             <form onSubmit = {handleSubmit} className="mx-auto w-[350px] h-[580px] bg-gray-100 space-y-3 rounded-xl shadow-md">
                <div className = "h-[100px] w-full bg-green-700 rounded-t-xl text-white pl-6 pt-4">
                    <p className="font-semibold text-[1.8rem]">Create account</p>
                    <p className = "">Please enter account details.</p>
                </div>
                <div className = "w-full px-6">
                    <div className="mt-6">
                        <label htmlFor="Username" className="block mb-2">
                            Username
                        </label>
                        <input
                            type="text"
                            name="usernameField"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter your username"
                            onChange={(e) => {
                                setUsername(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className="mt-4">
                        <label htmlFor="Email" className="block mb-2">
                            Email
                        </label>
                        <input
                            type="text"
                            name="emailField"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter email address"
                            onChange={(e) => {
                                setEmail(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className="mt-4">
                        <label htmlFor="Password" className="block mb-2">
                            Password
                        </label>
                        <input
                            type="text"
                            name="passwordField"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter password"
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className="mt-4">
                        <label htmlFor="StartingBalance" className="block mb-2">
                            Starting Balance
                        </label>
                        <input 
                            type = "text"
                            name = "balanceField"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            onChange={(e) => {
                                setBalance(e.target.value);
                                setMessage('');
                            }}
                            placeholder="Enter starting balance amount"
                        />
                    </div>
                    <div className = {clsx(
                        "text-red-500 mt-3 text-[0.9rem] opacity-0 h-[1.5rem]",
                        {
                            "opacity-100": message !== ''
                        }, 
                        {
                            "!text-green-700": message === "Account created successfully."
                        }
                        )} 
                    >
                        <p>{message}</p>
                    </div>
                    <div className="mt-0 text-white">
                        <button type = "submit" className = "w-full h-[2rem] bg-green-700 mt-3">Create a new account</button>
                        <button onClick = {() => updateIsCreatingStatus(false)} className = "w-full h-[2rem] bg-green-700 mt-3">Sign in Instead</button>
                    </div>
                </div>
             </form>
        </div>
    )
}

export default CreateForm;