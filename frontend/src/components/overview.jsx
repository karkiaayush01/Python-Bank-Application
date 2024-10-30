import { useEffect, useState } from "react";
import clsx from "clsx";
import LoadingPage from "./loading";

function Overview({userData}){
    const[isLoading, setIsLoading] = useState(true);
    const[transactionData, setTransactionData] = useState([])
    const[currentBalance, setCurrentBalance] = useState(0)
    
    useEffect(() => {
        const fetchData = async() => {
            const token = localStorage.getItem('access_token');
            try{
                setIsLoading(true);
                
                const balanceResponse = await fetch('http://localhost:8000/get-balance', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if(balanceResponse.ok){
                    const balanceResponseJson = await balanceResponse.json();   
                    setCurrentBalance(balanceResponseJson.balance);
                }
                else{
                    const errorData = await balanceResponse.json()
                    throw new Error(errorData.detail || "Error");
                }


                const transactionResponse = await fetch('http://localhost:8000/get-recent-transactions', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                })

                if(transactionResponse.ok){
                    const transactionResponseJson = await transactionResponse.json();   
                    setTransactionData(transactionResponseJson.Transactions);
                    setIsLoading(false);
                }
                else{
                    const errorData = await transactionResponse.json()
                    throw new Error(errorData.detail || "Error");
                }
            
            }
            catch(error){
                console.log(error.message)
            }
        };

        fetchData();
    }, []);

    if(isLoading){
        return(
            <LoadingPage />
        )
    }

    return(
        <div className="w-full p-[30px] font-[Poppins] text-green-700">
            <div className="flex h-[250px] mt-4 gap-10">
                <div className="bg-gray-100 rounded-lg w-[50%] pt-5 pl-7">
                    <h2 className="text-[2rem] font-[600]">Current Balance</h2>
                    <h1 className="text-[3rem] font-[600] mt-[70px]">Rs. {currentBalance}</h1>
                </div>
                <div className="bg-gray-100 rounded-lg w-[50%]"></div>
            </div>
            <div className="flex h-[350px] mt-10 gap-10">
                <div className = "w-[50%] bg-gray-100 rounded-lg py-5 px-7 flex flex-col justify-between">
                    <h1 className="text-[1.3rem] font-[600] mt-4">Recent Transactions</h1>
                    <div className="h-[80%] bg-white rounded-lg flex flex-col p-3 gap-1">
                        {Array.isArray(transactionData) && transactionData.length > 0 ? (
                            transactionData.map((transaction, index) => (
                                <div key = {index} className={clsx(
                                    "h-[20%] border-b-2 border-green-700 px-4 flex justify-between items-center",
                                    {"!text-red-500" : transaction.type === 'withdraw'}
                                )}
                                >
                                    <p>{transaction.type}<br />
                                        <span className="text-black mr-2">{transaction.dateTime.split('T')[0]}</span>
                                        <span className="text-black mr-2">{transaction.dateTime.split('T')[1].split('.')[0]}</span>
                                    </p>

                                    <p>Rs. {transaction.amount}</p>
                                </div>
                            ))
                        ): (
                            <div className="w-full h-full flex justify-center items-center">
                                <p className="text-center">No recent transactions.</p>
                            </div>
                        )}
                    </div>
                </div>
                <div className = "w-[50%] bg-gray-100 rounded-lg">
                </div>
            </div>
        </div>
    )
}

export default Overview;