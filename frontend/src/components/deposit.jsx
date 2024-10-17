import { useState } from "react";
import clsx from "clsx";


function Deposit(){

    const[amount, setAmount] = useState(0);
    const[message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try{
            if(e.target.elements.depositField.value === ''){
                throw new Error('Empty fields found.')
            }
            else if(Number(e.target.elements.depositField.value) == 0){
                throw new Error("Amount cannot be 0.")
            }
            const depositResponse = await fetch('http://localhost:8000/deposit', {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount
                })
            })

            if (!depositResponse.ok){
                throw new Error("An error occured.")
            }

            const depositResponseJson = await depositResponse.json();
            e.target.elements.depositField.value = '';
            setMessage(depositResponseJson.message);
        }
        catch(error){
            setMessage(error.message);
        }

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
            <h1 className="text-[2rem] font-[600]">Deposit Amount</h1>
            <form className="mt-4" onSubmit={handleSubmit}>
                <input
                    type='text'
                    placeholder='Enter deposit amount.'
                    className="h-[50px] w-full max-w-[500px] text-[1rem] pl-3 border border-gray-500 block"
                    onChange={handleChange}
                    name="depositField"
                />
                <p className={clsx(
                    'opacity-0 text-red-500 mt-2 h-[25px]',
                    {'opacity-100 !text-green-700' : message === 'Balance deposited successfully.'},
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

export default Deposit;