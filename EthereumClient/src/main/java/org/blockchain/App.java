package org.blockchain;

import org.blockchain.operations.Blockchain;
import org.reactivestreams.Subscription;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.http.HttpService;

import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;

public class App
{
    public static void main( String[] args ) throws NoSuchAlgorithmException, IOException, InterruptedException {
        Scanner in = new Scanner(System.in);

        String privateKey, destinationAddress, amountToBeSent, condition;

        Web3j client = Web3j.build(new HttpService("HTTP://127.0.0.1:7545"));

        System.out.print("Enter Y/N to continue with Transaction: ");
        condition = in.next();

        if(condition.equalsIgnoreCase("y")) {

            System.out.print("Enter Private Key: ");
            privateKey = in.next();

            System.out.print("Enter Destination Address: ");
            destinationAddress = in.next();

            System.out.print("Enter Amount to be sent: ");
            amountToBeSent = in.next();

            String transactionHash = Blockchain.doTransaction(client, privateKey, destinationAddress, amountToBeSent);
            System.out.println("Transaction Hash: " + transactionHash);
        }

        System.out.println("\nTransactions");
        Subscription subscription = (Subscription) client.replayPastTransactionsFlowable(DefaultBlockParameterName.EARLIEST, DefaultBlockParameterName.LATEST).subscribe(tx -> {
            System.out.println("Block Hash: " + tx.getBlockHash() + "\nTransaction Hash: " + tx.getHash() + "\nValue: " + tx.getValue() + "\n\n");
        });

        System.exit(0);

    }
}
