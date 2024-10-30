import { useState } from "react";
import clsx from "clsx";

const ConfirmationPage = ({updateConfirmationStatus, updateIsCreatingStatus, username}) => {
    const [confirmationCode, setConfirmationCode] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async(e) => {
        e.preventDefault();

        try{
            if(!confirmationCode){
                setMessage('Empty Field.');
            }

            const response = await fetch('http://localhost:8000/confirmation', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': username,
                    'confirmationCode':confirmationCode
                })
            });

            if(!response.ok){
                const errorData = await response.json();
                console.error(errorData);
                throw new Error(errorData.detail || 'An error occured.')
            }

            setMessage('Confirmed. Redirecting to sign in page....')
            setTimeout(() => {
                goBackToSignIn();
            }, 3000);
        }
        catch(err){
            setMessage(err.message);
        }
    }

    function goBackToSignIn(){
        updateConfirmationStatus(false);
        updateIsCreatingStatus(false);
    }

    return(
        <div className= "flex items-center justify-center w-full h-screen">
             <form onSubmit = {handleSubmit} className="mx-auto w-[350px] h-[380px] bg-gray-100 space-y-3 rounded-xl shadow-md">
                <div className = "h-[130px] w-full bg-green-700 rounded-t-xl text-white pl-6 pt-9">
                    <p className="font-semibold text-[1.8rem]">Confirm Email</p>
                    <p className = "">Please enter the code sent in mail.</p>
                </div>
                <div className = "w-full px-6">
                    <div className="mt-6">
                        <label htmlFor="Confirmation Code" className="block mb-2">
                            Confirmation Code
                        </label>
                        <input
                            type="text"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter Confirmation Code"
                            onChange={(e) => {
                                setConfirmationCode(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className = {clsx(
                        "text-red-500 mt-3 text-[0.9rem] opacity-0 h-[1.5rem]",
                        {
                            "opacity-100": message !== ''
                        },
                        {
                            "opacity-100 !text-green-500": message == 'Confirmed. Redirecting to sign in page....'
                        }
                        )} 
                    >
                        <p>{message}</p>
                    </div>
                    <div className="mt-4 text-white">
                        <button type="submit" className="w-full h-[2rem] bg-green-700 ">Confirm</button>
                        <button onClick = {goBackToSignIn} className = "w-full h-[2rem] bg-green-700 mt-3">Confirm Later</button>
                    </div>
                </div>
             </form>
        </div>
    )
}

export default ConfirmationPage;