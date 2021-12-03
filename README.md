# Smart Contract
A smart contract for a gym machine rental with various forms of transactions available for 
the owner and the customer.
 ## Writing the Smart Contract in Solidity
The bookings are stored in an array of a user defined data structure using the keyword ```struct```.
Each booking data structure contains the start time, the end time  (of the slots), the address
of the customer booking the slot, and the name of the machine that is booked. <br>
A constructor is used to predefine a set of machines in the gym, a list to which machines can
be added later at any time by the owner. A modifier is used to define onlyOwner that cna be used
in functions that are supposed to be called only by the owner. <br>
The functions are pretty well defined for their purpose, the ones used in this contract are,
1. **Book**<br>
   Pushes a new booking structure instance into the array of bookings.
2. **checkSlot**<br>
   Checks if access to a machine exists in the time slot specified.
3. **checkMachine**<br>
   Checks if a machine exists in the gym.
4. **checkAccess**<br>
   Checks if a machine is occupied at a specified time.
5. **checkTime**<br>
   Checks if the time entered is valid or not. This is not a public function, this is used only
   within the contract to verify the validity of the time entered.
6. **addMachine**<br>
   Adds a machine to the list of machines to choose from.
7. **setSlotPrice**<br>
   Only for the owner - Sets the price for each slot.
8. **withdraw**<br>
Allows the owner to withdraw the amount stored in the contract and transfer it to his wallet.

## Deploying the contract using web3.py
Web3.py is a Python library for interacting with Ethereum. The documentation can be found
[here](https://web3py.readthedocs.io/en/stable/).

### Requirements
1. Install solcx for compiling the solidity code
   ```
   pip install py-solc-x 
    ```
2. Install web3.py
    ```
    pip install web3
    ```
### Procedure of deploying the contract
* The solidity code is first compiled using ```compile_standard``` from solcx, which returns
  a json file.
* The abi and bytecode are obtained from the json file, which can be accessed using the 
```json``` library in python.
* Any function in the solidity code that involves a state change can only be called by making a transaction,
which takes some gas price. You can make and send a transaction using the following code 
  structure,
  ```
  contract = w3.eth.contract(abi=abi, bytecode=bytecode)
  nonce = w3.eth.getTransactionCount(address)
  Transaction = contract.constructor().buildTransaction(
      {
          "chainId": chain_id,
          "gasPrice": w3.eth.gas_price,
          "from": address,
          "nonce": nonce,
      }
  )
  signed_txn = w3.eth.account.sign_transaction(Transaction, private_key)
  txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
  ```
  The above code is used for deploying a contract, in order to call other functions in 
the solidity code,
  ```
  contract = w3.eth.contract(address=contract_address, abi=abi)
  nonce = w3.eth.getTransactionCount(address)
  Transaction = contract.functions.function_name(arguments).buildTransaction(
      {
          "chainId": chain_id,
          "gasPrice": w3.eth.gas_price,
          "from": address,
          "nonce": nonce,
          "value": value
      }
  )
  signed_txn = w3.eth.account.sign_transaction(Transaction, private_key=key)
  txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
  ```
  Using these two pieces of code, any function may be called and executed.
<br> (In deploy.py, the second half consists of code used to create a user interface to
  deploy and interact with a contract)
  
## Deployed Contract
I have deployed a contract in the Rinkeby test network, the contract address is given by
```0x1571690A35d4bBbe07693f6ea35bB02cCe6Aedf5```. The transactions made to and from the contract
can be viewed in [Rinkeby Etherscan](https://rinkeby.etherscan.io/address/0x1571690A35d4bBbe07693f6ea35bB02cCe6Aedf5). 

## Instructions
In order to test the smart contract, 
* Run ```deploy.py``` 
* If you want to deploy a new contract, type yes. If you want to interact with the contract that
is already deployed, type no.
* Type in your public and private keys, and then the contract address (if you don't want to deploy a new one) -
  ```0x1571690A35d4bBbe07693f6ea35bB02cCe6Aedf5```.
* You can now interact with the contract.