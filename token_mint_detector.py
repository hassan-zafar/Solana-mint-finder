import json
import sys

# Raydium constants
RAYDIUM_KEYWORD = "initialize2"
RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

# Token Program constants
TOKEN_KEYWORD = "InitializeMint"
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

def extract_contract_address(instruction):
    token_balances = instruction.get("tokenBalances")
    if token_balances and isinstance(token_balances, list):
        for token in token_balances:
            if "mint" in token:
                return token["mint"]
    return None

def process_block(block):
    transactions = []
    for group in block.get("data", []):
        if isinstance(group, list):
            transactions.extend(group)
        else:
            transactions.append(group)
    
    for tx in transactions:
        logs = tx.get("logs", [])
        
        lower_logs = [log.lower() for log in logs]
        
        # Check if Raydium "initialize2" is present
        if any(RAYDIUM_KEYWORD in log for log in lower_logs):
            print("New Raydium token mint (liquidity pool creation) transaction detected!")
            signature = tx.get("signature")
            print("Transaction Signature:", signature)
            
            # Look for the Raydium program invocation
            for invocation in tx.get("programInvocations", []):
                program_id = invocation.get("programId", "")
                if program_id == RAYDIUM_PROGRAM_ID:
                    print(" → Raydium program invocation found:")
                    instruction = invocation.get("instruction", {})
                    print("   Instruction details:", instruction)
                    # Extract contract address from the instruction
                    ca = extract_contract_address(instruction)
                    if ca:
                        print("   Token Contract Address (CA):", ca)
                    else:
                        print("   Token Contract Address not found in instruction.")
            print("-" * 50)
        
        #(ADDING IT JUST TO BE SURE I DON'T THINK IT WAS IN THE ASKED QUESTION)
        if any(TOKEN_KEYWORD.lower() in log for log in lower_logs):
            print("New token mint transaction detected!")
            signature = tx.get("signature")
            print("Transaction Signature:", signature)

            for invocation in tx.get("programInvocations", []):
                program_id = invocation.get("programId", "")
                if program_id == TOKEN_PROGRAM_ID:
                    print(" → SPL Token Program invocation found:")
                    instruction = invocation.get("instruction", {})
                    print("   Instruction details:", instruction)
                    ca = extract_contract_address(instruction)
                    if ca:
                        print("   Token Contract Address (CA):", ca)
                    else:
                        print("   Token Contract Address not found in instruction.")

            print("-" * 50)

def main():
    if len(sys.argv) < 2:
        print("Usage: python token_mint_detector.py <block_file.json>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            block = json.load(f)
    except Exception as e:
        print("Error reading JSON file:", e)
        sys.exit(1)
    
    process_block(block)

if __name__ == "__main__":
    main()
