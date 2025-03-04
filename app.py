import streamlit as st
from web3 import Web3

# Connect to Blockchain (Ganache or Infura)
ganache_url = "https://your-ngrok-url.ngrok.io"  # Replace with your actual Ngrok URL
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Load Smart Contract
contract_address = "0x8996Bc59A4bB51f230F07305a9215DFA267A94f2"  # Replace with your deployed contract address
abi = [
    {
        "inputs": [],
        "name": "candidatesCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_candidateId", "type": "uint256"}],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

]
]  # Paste your contract ABI here
election_contract = w3.eth.contract(address=contract_address, abi=abi)

# Streamlit UI
st.title("🗳️ Blockchain-Based Voting System")

# Get Candidates
candidates_count = election_contract.functions.candidatesCount().call()
candidates = [election_contract.functions.candidates(i).call() for i in range(1, candidates_count + 1)]

# Display Candidates
st.header("🔹 Candidates")
for candidate in candidates:
    st.write(f"**{candidate[0]}. {candidate[1]}** - Votes: {candidate[2]}")

# Voting Section
st.header("🗳️ Cast Your Vote")
selected_candidate = st.selectbox("Select a candidate", [c[0] for c in candidates])
if st.button("Vote"):
    txn = election_contract.functions.vote(selected_candidate).build_transaction({
        "from": w3.eth.accounts[0],  # Use an account from Ganache
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(w3.eth.accounts[0]),
    })
    signed_txn = w3.eth.account.sign_transaction(txn, "0x98f5615e35b439d4ff7e03362ab909cb913d03afc94dad9de22ffc3cd2527d67")  # Replace with Ganache private key
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    st.success(f"✅ Vote Casted Successfully! Transaction Hash: {txn_hash.hex()}")

# Real-time Results
if st.button("🔄 Refresh Results"):
    candidates = [election_contract.functions.candidates(i).call() for i in range(1, candidates_count + 1)]
    st.experimental_rerun()

