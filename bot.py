import time
from solana.account import Account
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.system_program import transfer
from solana.transaction import Transaction

# Static Solana wallet address and private key
STATIC_WALLET_ADDRESS = "BK5yVX21zgmCBQtRQrNZU3uRKLXEeJKgPD7j6aJkdyJg"
STATIC_PRIVATE_KEY = "ZFYjndFpH43xPpojxa37kv74m5m6jQhKnK18PM6fSzM41obB4ftVvdUfRAjoVFNbHV1oYLnRGcRgFX3egNEQJwi"

# Destination wallet address
DESTINATION_ADDRESS = "CXjGBG7P7c7XzV74M68hoFeu3z2wibv4jR86bc6kT4Mo"

# Solana RPC endpoint
RPC_ENDPOINT = 'https://api.mainnet-beta.solana.com'

# Initialize Solana RPC client
solana_client = Client(RPC_ENDPOINT)

def check_transactions():
    while True:
        # Get current balance of the static wallet address
        balance = get_wallet_balance(STATIC_WALLET_ADDRESS)
        
        # If balance is greater than 0, initiate transfer to DESTINATION_ADDRESS
        if balance > 0:
            try:
                # Transfer SOL from STATIC_WALLET_ADDRESS to DESTINATION_ADDRESS
                transfer_sols(STATIC_PRIVATE_KEY, STATIC_WALLET_ADDRESS, DESTINATION_ADDRESS, balance)
                
                # Log the transaction
                print(f"Transferred {balance} SOL from {STATIC_WALLET_ADDRESS} to {DESTINATION_ADDRESS}")
                
                # Update wallet balance to 0 (for demonstration purposes)
                # Note: You may need more robust logic in a production environment.
                
            except Exception as e:
                print(f"Error transferring SOL: {e}")
        
        # Wait for 10 seconds before checking again
        time.sleep(10)

def get_wallet_balance(wallet_address: str) -> float:
    try:
        # Get balance in SOL (lamports to SOL conversion)
        lamports = solana_client.get_balance(wallet_address)['result']['value']
        sol_balance = lamports / 10**9  # Convert lamports to SOL
        return sol_balance
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
        return 0.0

def transfer_sols(private_key: str, sender_address: str, recipient_address: str, amount: float):
    try:
        # Create sender's account object
        sender_account = Account(private_key)
        
        # Construct the transaction
        transaction = Transaction(
            recent_blockhash=solana_client.get_recent_blockhash()['result']['value']['blockhash'],
            fee_payer=sender_account.public_key(),
            instructions=[
                transfer(
                    sender_address,
                    sender_account.public_key(),
                    recipient_address,
                    amount * 10**9  # Convert SOL to lamports
                ),
            ],
        )

        # Sign the transaction
        transaction.sign(sender_account)

        # Send the transaction
        tx_hash = solana_client.send_transaction(transaction, opts=TxOpts(skip_confirmation=False))
        
        # Wait a bit to ensure transaction is processed (optional)
        time.sleep(5)

    except Exception as e:
        raise RuntimeError(f"Failed to transfer SOL: {e}")

if __name__ == '__main__':
    check_transactions()
