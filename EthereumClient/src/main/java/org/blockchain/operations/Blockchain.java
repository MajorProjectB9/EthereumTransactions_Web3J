package org.blockchain.operations;

import org.web3j.crypto.Credentials;
import org.web3j.crypto.RawTransaction;
import org.web3j.crypto.TransactionEncoder;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.response.*;
import org.web3j.utils.Convert;
import org.web3j.utils.Numeric;

import java.io.IOException;
import java.math.BigInteger;
import java.util.Optional;

public class Blockchain
{

    public static String doTransaction(Web3j client, String privateKey, String destinationAddress, String amountToBeSent) throws IOException, InterruptedException {
        Credentials credentials = Credentials.create(privateKey);

        EthGetTransactionCount ethGetTransactionCount = client.ethGetTransactionCount(credentials.getAddress(), DefaultBlockParameterName.LATEST).send();
        BigInteger nonce = ethGetTransactionCount.getTransactionCount();

        BigInteger value = Convert.toWei(amountToBeSent, Convert.Unit.ETHER).toBigInteger();

        BigInteger gasLimit = BigInteger.valueOf(21000);
        BigInteger gasPrice = Convert.toWei("1", Convert.Unit.GWEI).toBigInteger();

        RawTransaction rawTransaction = RawTransaction.createEtherTransaction(nonce, gasPrice, gasLimit, destinationAddress, value);

        byte[] signedMessage = TransactionEncoder.signMessage(rawTransaction, credentials);
        String hexValue = Numeric.toHexString(signedMessage);

        EthSendTransaction ethSendTransaction = client.ethSendRawTransaction(hexValue).send();
        String transactionHash = ethSendTransaction.getTransactionHash();

        Optional<TransactionReceipt> transactionReceipt = null;
        do {
            System.out.println("Checking if transaction " + transactionHash + " is mined….");
            EthGetTransactionReceipt ethGetTransactionReceiptResp = client.ethGetTransactionReceipt(transactionHash)
                    .send();
            transactionReceipt = ethGetTransactionReceiptResp.getTransactionReceipt();
            Thread.sleep(3000);
        } while (!transactionReceipt.isPresent());

        System.out.println("Transaction " + transactionHash + " was mined in block # " + transactionReceipt.get().getBlockNumber());
        System.out.println("Balance: " + Convert.fromWei(client.ethGetBalance(credentials.getAddress(), DefaultBlockParameterName.LATEST).send().getBalance().toString(), Convert.Unit.ETHER));

        return transactionHash;
    }

}
