import web3
from web3 import Web3
from solcx import compile_source

# Solidity source code
f = open("todo_list.sol", "r")
x = f.read()
compiled_sol = compile_source(x,output_values=['abi', 'bin'])

# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

# web3.py instance
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[0]
# w3.eth.default_account = '0x55c18fbF72EBcb055082104fab3840807F680a78'

TODO_LIST = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = TODO_LIST.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

TODO_LIST = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)


tx_hash = TODO_LIST.functions.createTask("Get up from sleep!").transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_hash)

# Can further iterate the tx_receipt
print(tx_receipt)


# print(TODO_LIST.functions.getTask(2).call())
# print(TODO_LIST.functions.toggleCompleted(2).call())
# print(TODO_LIST.functions.getTask(2).call())


def create_task(task):
    TODO_LIST.functions.createTask(task).transact()

def get_task(x):
    task = (TODO_LIST.functions.getTask(x).call())
    return task

def toggle_Completed(x):
    task = TODO_LIST.functions.toggleCompleted(x).transact()
    return task

#
# create_task("Go to office!")
# get_task(2)
# toggle_Completed(3)
# get_task(3)

