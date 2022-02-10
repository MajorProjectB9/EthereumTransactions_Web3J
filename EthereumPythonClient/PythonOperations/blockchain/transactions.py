from web3 import Web3
import numpy as np


class Blockchain:

    def __init__(self):
        ganache_url = 'HTTP://127.0.0.1:7545'
        self.__web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.__sender = '0x963a8f95bA094fF6Fa9ED0338eB01618a2DE4595'
        self.__private_key = '471b664a7684336faef08a9a03d5f0534d2df5eac84247453a33041e9599e97e'
        self.__recipient = ""
        self.__amount = ""
        self.__reason = ""

    def get_web3(self):
        return self.__web3

    def get_sender(self):
        return self.__sender

    def get_private_key(self):
        return self.__private_key

    def set_recipient(self, recipient_address, amount, reason):
        self.__recipient = recipient_address
        self.__amount = amount
        self.__reason = reason

    def get_block_details(self):
        transaction_count = self.__web3.eth.getTransactionCount(self.__sender)
        blocks = []
        for i in range(transaction_count + 1):
            blocks.append(self.__web3.eth.getBlock(i))
        return blocks

    def get_transaction_hashes(self):
        blocks = self.get_block_details()
        transaction_hashes = []
        for t in blocks:
            s = str(t)
            s = s[15:-3]
            res = []
            res = s.split(', ')
            transaction_hashes.append(res[18][27:-3])
        return transaction_hashes

    def get_transactions_details(self):
        count = 0
        rows = self.__web3.eth.getTransactionCount(self.__sender)
        parsed_transactions = np.ndarray(shape=(rows, 4), dtype=object)
        transaction_hashes = self.get_transaction_hashes()
        for tx in transaction_hashes:
            if count > 0:
                t = self.__web3.eth.getTransaction(tx)
                for i in range(0, rows):
                    parsed_transactions[i][0] = self.__web3.toHex(t["hash"])
                    parsed_transactions[i][1] = t["from"]
                    parsed_transactions[i][2] = t["to"]
                    parsed_transactions[i][3] = t["value"]

            count += 1
        return parsed_transactions

    def do_transaction(self, address_receiver, value):
        nonce = self.get_web3().eth.getTransactionCount(self.__sender)
        tx = {
            'nonce': nonce,
            'to': address_receiver,
            'value': self.__web3.toWei(value, 'ether'),
            'gas': 2000000,
            'gasPrice': self.__web3.toWei('50', 'gwei')
        }
        signed_tx = self.__web3.eth.account.sign_transaction(tx, self.__private_key)
        tx_hash = self.__web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash
