import web3.eth
from web3 import Web3
from solcx import compile_source

# Need to install the solidity compiler here, this is the code for that ----------------------
from solcx import compile_standard, install_solc
install_solc("0.6.0")
# -----------------------------------------------------------------------------------------------

# connecting to a node
eth = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(eth))
chain_id = 1337
print("This the status of your connection to the blockchain: " + str(w3.isConnected()))

my_address = "0x6F3247E315d5Be9EA74e77f9e29D0C006606f2A1"
private_key = "0x41453a468617df9f2d2db87b69bd5bb0540e217ee4f0dadacaa2707238a4b1ca"

# Solidity source code
# ------------------------------------------------------------------------
f = open("todo_list.sol", "r")
x = f.read()
compiled_sol = compile_source(x,output_values=['abi', 'bin'])
# ------------------------------------------------------------------------

# retrieve the contract interface -----------------------------------------
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin ----------------
bytecode = contract_interface['bin']
print("This is the bytecode ------------------>")
print(bytecode)
# get abi ---------------------------
abi = contract_interface['abi']
print("This is the ABI ------------------------>")
print(abi)

# The compiled code ------------------------------------
print("This is the compiled code ------------------>")
compiled_sol = compile_source(x,output_values=['abi', 'bin'])



# set pre-funded account as sender, this gives us the first account in the list of accounts
w3.eth.default_account = w3.eth.accounts[0]
print("This is the default account: " + str(w3.eth.default_account))

# Creating the contract object ------------------------------------------------------
TODOLIST = w3.eth.contract(abi=abi, bytecode=bytecode)
print(" This is the TODO_LIST contract : " + str(TODOLIST))

# Get the latest transactionCount --------------------
nonce = w3.eth.getTransactionCount(my_address)



# Submit the transaction that deploys the contract ------------------------------------
transaction = TODOLIST.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Sign the transaction ------------------------------------------------------------------
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# Sending the transaction ----------------------------------------------------------------
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
# -----------------------------------------------------------------------------------------


# Submit the transaction that deploys the contract-------------------------------------
tx_hash = TODOLIST.constructor().transact()
print("The transaction has occurred and this is the transaction hash: ")
print(tx_hash)


# Calling the greet function -----------------------
# Working with deployed Contracts
TODOLIST = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"This is the get_no_sales function:  {TODOLIST.functions.getTask(1).call()}")

# Calling the setGreeting function--------------------------------------------------------------------
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("This is the other transaction hash: " + str(tx_hash))

# Can further iterate the tx_receipt-----------------------
print("This is the transaction receipt")
print(tx_receipt)


# Calling the make_sale_record function -------------------------
print("This is the return from the make_sale_record() function: " )
print(TODOLIST.functions.createTask("Attend meeting").transact())
print("Data type of this return is: " + str(type(TODOLIST.functions.createTask("Attend meeting").transact())))


#  -------------------------------------------------------------
# Reading from the smart contract
# This function is getting us the state variable called greeting
SALE_NUMBER = TODOLIST.functions.getTask(1).call()
print("This is the number of sales : " + str(SALE_NUMBER))


# Make  new Transaction using functions ------------------>
def create_task(task):
    TODOLIST.functions.createTask(task).transact()

def get_task(x):
    task = (TODOLIST.functions.getTask(x).call())
    return task

def toggle_Completed(x):
    task = TODOLIST.functions.toggleCompleted(x).transact()
    return task

print("this is the task:")
print(get_task(1))
