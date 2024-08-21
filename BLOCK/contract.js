const axios = require('axios');
const Web3 = require('web3');
const { abi, address } = require('./contract'); // Your contract's ABI and address
const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'); // Ethereum Node

// Firebase Database URL
const FIREBASE_URL = 'https://console.firebase.google.com/u/0/project/iam-dashborad/database/iam-dashborad-default-rtdb/data/~2F';

// Ethereum Account Credentials
const account = web3.eth.accounts.privateKeyToAccount('YOUR_PRIVATE_KEY');
web3.eth.accounts.wallet.add(account);
web3.eth.defaultAccount = account.address;

const contract = new web3.eth.Contract(abi, address);

async function updateSmartContract() {
    try {
        // Fetch data from Firebase
        const response = await axios.get(FIREBASE_URL);
        const data = response.data;

        // Calculate keccak256 hash of the data
        const hash = web3.utils.keccak256(JSON.stringify(data));

        // Get the current hash from the contract
        const currentHash = await contract.methods.currentHash().call();

        // If hashes differ, update the smart contract
        if (currentHash !== hash) {
            const tx = contract.methods.updateHash(web3.utils.fromAscii(hash));

            // Estimate gas
            const gas = await tx.estimateGas({ from: account.address });
            
            // Send the transaction
            const receipt = await tx.send({ from: account.address, gas });
            console.log('Hash updated:', receipt);
        } else {
            console.log('Hash is already up to date.');
        }
    } catch (error) {
        console.error('Error updating smart contract:', error);
    }
}

// Run every 10 seconds
setInterval(updateSmartContract, 10000);
