import { useState } from "react";
import { clsx } from "clsx";

function CreateForm({updateIsCreatingStatus}){
    const [username, setUsername] = useState('');
    const [pincode, setPincode] = useState('');
    const [balance, setBalance] = useState('');
    const [message, setMessage] = useState('');


    const handleSubmit = async (e) => {
        e.preventDefault(); 

        try{
            if(isNaN(Number(pincode))){
                throw new Error('Pincode should be only numbers.')
            }

            if (balance === ''){
                throw new Error('Empty Fields Found.')
            }
            else if (isNaN(Number(balance))){
                throw new Error('Invalid balance amount.')
            }

            const response = await fetch('http://localhost:8000/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    pincode,
                    balance
                }),
            });
            
            if (!response.ok){
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login Failed');
            }

            const data = await response.json();
            setMessage(data.message);

            e.target.elements.usernameField.value = '';
            setUsername('');
            e.target.elements.pincodeField.value = '';
            setPincode('');
            e.target.elements.balanceField.value = '';
            setBalance('');
        }
        catch(error){
            setMessage(error.message);
        }
    }
    return(
        <div className= "flex items-center justify-center w-full h-screen">
             <form onSubmit = {handleSubmit} className="mx-auto w-[350px] h-[500px] bg-gray-100 space-y-3 rounded-xl shadow-md">
                <div className = "h-[100px] w-full bg-green-700 rounded-t-xl text-white pl-6 pt-4">
                    <p className="font-semibold text-[1.8rem]">Create account</p>
                    <p className = "">Please enter account details.</p>
                </div>
                <div className = "w-full px-6">
                    <div className="mt-6">
                        <label htmlFor="Email" className="block mb-2">
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
                        <label htmlFor="Pincode" className="block mb-2">
                            Pincode
                        </label>
                        <input
                            type="text"
                            name="pincodeField"
                            className="border-[0.1rem] rounded-sm focus:border-green-700 focus:outline-none pl-2 text-sm h-8 w-full"
                            placeholder = "Enter 4 digit pincode"
                            onChange={(e) => {
                                setPincode(e.target.value);
                                setMessage('');
                            }}
                        />
                    </div>
                    <div className="mt-4">
                        <label htmlFor="Pincode" className="block mb-2">
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
                        <button className = "w-full h-[2rem] bg-green-700 mt-3">Create a new account</button>
                        <button onClick = {() => updateIsCreatingStatus(false)} className = "w-full h-[2rem] bg-green-700 mt-3">Sign in Instead</button>
                    </div>
                </div>
             </form>
        </div>
    )
}

export default CreateForm;