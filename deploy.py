from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

# Loading the dotenv module in order to be able to load environment variables from the .env file
load_dotenv()

# Loading the data from the contract file
with open("./GMRSmartContract.sol", "r") as f:
    source_code = f.read()

# Installing the library that will help in compiling and returning useful information from the source_code
install_solc("v0.6.0")

# Compiling the solidity file
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"GMRSmartContract.sol": {"content": source_code}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}},
    },
    solc_version="v0.6.0",
)

# Dumping the json file into a variable
with open("./compiled_code.json", "w") as f:
    json.dump(compiled_sol, f)

# Getting the abi and the bytecode from the compiled_sol variable
abi = compiled_sol["contracts"]["GMRSmartContract.sol"]["GMRSmartContract"]["abi"]
bytecode = compiled_sol["contracts"]["GMRSmartContract.sol"]["GMRSmartContract"]["evm"][
    "bytecode"
]["object"]

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/ea00e54ec41644a7bb9fcda90ded82cd"))
chain_id = 4


class Transaction:
    def __init__(self):
        self.receipt = None
        self.slotPrice = 100

    def deploy(self, address, key):
        deploy_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = w3.eth.getTransactionCount(address)
        deploy_transaction = deploy_contract.constructor().buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": address,
                "nonce": nonce,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(deploy_transaction, private_key=key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    def book(self, address, key, contract_address, machine_name, start_time, end_time):
        booking_contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(address)
        booking_transaction = booking_contract.functions.book(machine_name, start_time, end_time).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": address,
                "nonce": nonce,
                "value": self.slotPrice
            }
        )
        signed_txn = w3.eth.account.sign_transaction(booking_transaction, private_key=key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    def checkSlot(self, address, key, contract_address, machine_name, start_time, end_time):
        check_slot_contract = w3.eth.contract(address=contract_address, abi=abi)
        return check_slot_contract.functions.checkSlot(machine_name, start_time, end_time).call()

    def checkMachine(self, address, key, contract_address, machine_name):
        check_machine_contract = w3.eth.contract(address=contract_address, abi=abi)
        return check_machine_contract.functions.checkMachine(machine_name).call()

    def checkAccess(self, address, key, contract_address, machine_name, time):
        check_access_contract = w3.eth.contract(address=contract_address, abi=abi)
        return check_access_contract.functions.checkAccess(machine_name, time).call()

    def addMachine(self, address, key, contract_address, machine_name):
        add_machine_contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(address)
        add_machine_transaction = add_machine_contract.functions.addMachine(machine_name).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": address,
                "nonce": nonce,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(add_machine_transaction, private_key=key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    def setSlotPrice(self, address, key, contract_address, slot_price):
        slot_price_contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(address)
        slot_price_transaction = slot_price_contract.functions.setSlotPrice(slot_price).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": address,
                "nonce": nonce,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(slot_price_transaction, private_key=key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.slotPrice = slot_price
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    def withdraw(self, address, key, contract_address):
        withdraw_contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(address)
        withdraw_transaction = withdraw_contract.functions.withdraw(address).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": address,
                "nonce": nonce,
                "value": w3.eth.get_balance(self.receipt.contractAddress)
            }
        )
        signed_txn = w3.eth.account.sign_transaction(withdraw_transaction, private_key=key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)


print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t SMART CONTRACT")
deploy_new_contract = input("Would you like to deploy a new contract? : ")

if deploy_new_contract.upper() == 'YES':
    account_address = input("Type in your public key : ")
    private_key = input("Type in your private key : ")
    new_contract = Transaction()
    new_contract.deploy(address=account_address, key=private_key)
    print(f"The newly deployed contract has the address {new_contract.receipt.contractAddress}.")
    while True:
        print("\tYou have the following options,")
        print("\t\t\t1)Booking a time slot\n\t\t\t2)Check if a time slot is available\n\t\t\t3)Check if a certain "
              "machine exists\n\t\t\t4)Check if you have access to any particular machine at a specific time\n\t\t\t"
              "5)Add a new machine to the gym\n\t\t\t6)Set the price for one time slot\n\t\t\t7)Withdraw from the "
              "contract\n\t\t\t8)Exit")
        choice = int(input("Input a choice from the above : "))
        if choice == 1:
            print("\t The machines in the gym are as follows,")
            print("\t\t\t1.A\n\t\t\t2.B\n\t\t\t3.C\n\t\t\t4.D")
            machineName = input("Pick a machine : ")
            print(f"You will have access to {machineName} for a time slot of 30 mins. Pick a time slot. (Time entered "
                  f"must be in the military time format).")
            startTime = int(input("Start Time : "))
            endTime = int(input("End Time : "))
            new_contract.book(account_address, private_key, new_contract.receipt.contractAddress, machineName,
                              startTime, endTime)
            print(f"This has cost you {new_contract.slotPrice} wei.")
            print(f"You have booked {machineName} for the time slot between {startTime} and {endTime}.")
            print("-------------------------------------------------------------------")
        elif choice == 2:
            print("\t The machines in the gym are as follows,")
            print("\t\t\t1.A\n\t\t\t2.B\n\t\t\t3.C\n\t\t\t4.D")
            machineName = input("Pick a machine : ")
            startTime = int(input("Start Time : "))
            endTime = int(input("End Time : "))
            if new_contract.checkSlot(account_address, private_key, new_contract.receipt.contractAddress, machineName,
                                      startTime, endTime):
                print("Access exists!")
            else:
                print("Access does not exist.")
            print("-------------------------------------------------------------------")
        elif choice == 3:
            machineName = input("Pick a machine : ")
            if new_contract.checkMachine(account_address, private_key, new_contract.receipt.contractAddress,
                                         machineName):
                print(f"Machine '{machineName}' exists!")
            else:
                print(f"Machine '{machineName}' does not exist.")
            print("-------------------------------------------------------------------")
        elif choice == 4:
            machineName = input("Pick a machine : ")
            time = int(input("Time : "))
            if new_contract.checkAccess(account_address, private_key, new_contract.receipt.contractAddress, machineName,
                                        time):
                print("You have access!")
            else:
                print("You do not have access.")
            print("-------------------------------------------------------------------")
        elif choice == 5:
            machineName = input("Pick a machine : ")
            new_contract.addMachine(account_address, private_key, new_contract.receipt.contractAddress, machineName)
            print(f"Machine {machineName} has been added!")
            print("-------------------------------------------------------------------")
        elif choice == 6:
            price = int(input("Enter the price for one time slot : "))
            new_contract.setSlotPrice(account_address, private_key, new_contract.receipt.contractAddress, price)
            print("-------------------------------------------------------------------")
        elif choice == 7:
            contract_balance = w3.eth.get_balance(new_contract.receipt.contractAddress)
            new_contract.withdraw(account_address, private_key, new_contract.receipt.contractAddress)
            print(f"{contract_balance} wei has been transferred to your wallet.")
            print("-------------------------------------------------------------------")
        elif choice == 8:
            break
else:
    account_address = input("Type in your public key : ")
    private_key = input("Type in your private key : ")
    contract_address = input("Type in the contract address you would like to interact with : ")
    contract = Transaction()
    while True:
        print("\tYou have the following options,")
        print("\t\t\t1)Booking a time slot\n\t\t\t2)Check if a time slot is available\n\t\t\t3)Check if a certain "
              "machine exists\n\t\t\t4)Check if you have access to any particular machine at a specific time\n\t\t\t"
              "5)Exit")
        choice = int(input("Input a choice from the above : "))
        if choice == 1:
            print("\t The machines in the gym are as follows,")
            print("\t\t\t1.A\n\t\t\t2.B\n\t\t\t3.C\n\t\t\t4.D")
            machineName = input("Pick a machine : ")
            print(f"You will have access to {machineName} for a time slot of 30 mins. Pick a time slot. (Time entered "
                  f"must be in the military time format).")
            startTime = int(input("Start Time : "))
            endTime = int(input("End Time : "))
            contract.book(account_address, private_key, contract_address, machineName, startTime, endTime)
            print(f"This has cost you {contract.slotPrice} wei.")
            print(f"You have booked {machineName} for the time slot between {startTime} and {endTime}.")
            print("-------------------------------------------------------------------")
        elif choice == 2:
            print("\t The machines in the gym are as follows,")
            print("\t\t\t1.A\n\t\t\t2.B\n\t\t\t3.C\n\t\t\t4.D")
            machineName = input("Pick a machine : ")
            startTime = int(input("Start Time : "))
            endTime = int(input("End Time : "))
            if contract.checkSlot(account_address, private_key, contract_address, machineName, startTime, endTime):
                print("Access exists!")
            else:
                print("Access does not exist.")
            print("-------------------------------------------------------------------")
        elif choice == 3:
            machineName = input("Pick a machine : ")
            if contract.checkMachine(account_address, private_key, contract_address, machineName):
                print(f"Machine '{machineName}' exists!")
            else:
                print(f"Machine '{machineName}' does not exist.")
            print("-------------------------------------------------------------------")
        elif choice == 4:
            machineName = input("Pick a machine : ")
            time = int(input("Time : "))
            if contract.checkAccess(account_address, private_key, contract_address, machineName, time):
                print("You have access!")
            else:
                print("You do not have access.")
            print("-------------------------------------------------------------------")
        elif choice == 5:
            break
