import clsx from "clsx";
import { useState } from "react";

function Withdraw(){
    const [message, setMessage] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = async(e) => {
        e.preventDefault();

        try{
            if(e.target.elements.withdrawField.value === ''){
                throw new Error("Empty fields found.")
            }
            else if(Number(e.target.elements.withdrawField.value) == 0){
                throw new Error("Amount cannot be 0.")
            }
            const token = localStorage.getItem('access_token')
            const withdrawResponse = await fetch('http://localhost:8000/withdraw', {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    amount
                })

            })

            if (!withdrawResponse.ok){
                const withdrawResponseJson = await withdrawResponse.json();
                throw new Error(withdrawResponseJson.detail || 'An error occured.')
            }
            const withdrawResponseJson = await withdrawResponse.json();
            setMessage(withdrawResponseJson.message);
        }
        catch(error){
            setMessage(error.message);
        }

        e.target.elements.withdrawField.value = '';
    }

    function handleChange(e){
        var fieldValue = e.target.value;
        if(isNaN(Number(fieldValue))){
            if(fieldValue.length == 1){
                e.target.value = ''
            }
            else{
                e.target.value = fieldValue.slice(0, -1);
                setAmount(Number(e.target.value));
            }
        }
        else if (fieldValue.length >= 10){
            e.target.value = fieldValue.slice(0, -1);
            setAmount(Number(e.target.value));
        }
        else{
            setAmount(Number(e.target.value));
        }

        setMessage('');
    }

    return(
        <div className="w-full p-[80px] font-[Poppins]">
            <h1 className="text-[2rem] font-[600]">Withdraw Amount</h1>
            <form className="mt-4" onSubmit={handleSubmit}>
                <input
                    type='text'
                    placeholder='Enter withdrawal amount.'
                    className="h-[50px] w-full max-w-[500px] text-[1rem] pl-3 border border-gray-500 block"
                    onChange={handleChange}
                    name="withdrawField"
                />
                <p className={clsx(
                    'opacity-0 mt-2 h-[25px] text-red-500',
                    {'opacity-100 !text-green-700' : message === 'Balance withdrawn successfully.'},
                    {'opacity-100' : message !== ''}
                )}>
                    {message}
                </p>
                <button 
                    className="mt-2 h-[40px] bg-white border border-black px-4 font-[500] hover:bg-black hover:text-white"
                    type = "submit"
                >
                    Submit
                </button>
            </form>
        </div>
    )   
}

export default Withdraw;