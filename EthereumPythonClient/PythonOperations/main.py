
from blockchain.transactions import Blockchain


def main():
    blockchain = Blockchain()
    web3 = blockchain.get_web3()

    while 1:
        choice = input("1: Receive Transaction\n2: Retrieve All Blocks\n3: Retrieve All Transactions\n4: "
                       "Exit\nEnter Your Choice: ")

        if choice == "1":
            account_2 = input("Enter Your Address: ")
            value = input("Enter Amount the you want: ")
            print(blockchain.do_transaction(account_2, value))
            print("Received Fund")
        if choice == "2":
            blocks = blockchain.get_block_details()
            for b in blocks:
                print(b, "\n")
        if choice == "3":
            transactions = blockchain.get_transactions_details()
            i = 0
            for t in transactions:
                i += 1
                print("Transaction ", i)
                print("Transaction Hash: ", t[0], "\nSent To: ", t[2], "\nAmount Send (in Ether): ", t[3], "\n\n")

        if choice == "4":
            exit(0)


if __name__ == '__main__':
    main()

# from web3 import Web3
#
# web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
# private_key = '471b664a7684336faef08a9a03d5f0534d2df5eac84247453a33041e9599e97e'
# from_address = '0x963a8f95bA094fF6Fa9ED0338eB01618a2DE4595'
# to_address = '0x0c81667C713ef31B45eb3CA2DbfFB9B61be5A32b'
#
# nonce = web3.eth.getTransactionCount(from_address)
# gasPrice = web3.toWei('50', 'gwei')
# value = web3.toWei(0.1, 'ether')
#
# tx = {
#     'nonce': nonce,
#     'to': to_address,
#     'value': value,
#     'gas': 2000000,
#     'gasPrice': gasPrice
# }
#
# signed_tx = web3.eth.account.sign_transaction(tx, private_key)
# tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

