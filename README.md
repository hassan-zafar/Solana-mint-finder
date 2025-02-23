# **Solana Mint Finder**

## **1. Approach**

1. **Reading the Block File**  
   - The script takes a JSON file (decoded Solana block) as input.
   - I parse it using `json.load` to get the block object.

2. **Iterating Through Transactions**  
   - I look for the `data` field in the decoded block and flatten it (since it might be a list of lists or just a list).
   - Each element in this list represents a transaction.

3. **Scanning Logs**  
   - I examine the `logs` array within each transaction.  
   - I check for two things:
     - `initialize2` (for Raydium Liquidity Pool creation).
     - `InitializeMint` (for SPL Token Program mint creation).
   - If I find the relevant substring in any log line, I flag that transaction as a **new token creation**.

4. **Extracting Program Invocations**  
   - Within the same transaction, I look at the `programInvocations` array.
   - I match the **Raydium Program ID** (`675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`) for Raydium liquidity pool tokens, or the **SPL Token Program ID** (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) for general token mints.
   - If I find a matching invocation, I print details about the instruction.

5. **Contract Address Extraction**  
   - I attempt to parse the `instruction` object for a `"tokenBalances"` field.  
   - If present, I look for a `"mint"` key, which I treat as the **unique contract address** of the newly minted token.

6. **Printing the Transaction Signature**  
   - Finally, I print the transaction `signature` whenever I identify a new mint, fulfilling the core requirement.

---

## **2. Challenges Faced**

- **Identifying the Correct Logs**  
  - The original hint mentioned `"initialize"`, but in practice, Raydium can use `"initialize2"`. I had to adjust and confirm the correct log substring by analyzing real-world data.  
- **Decoding Variations**  
  - Different transactions sometimes place critical data in different fields (like `tokenBalances` vs. other custom fields). I had to create a generalized approach to extract the contract address without relying on a single schema.

---

## **3. How I Overcame Them**

- **Adjusting Log Keywords**  
  - I tested real Solana transactions (via explorers and sample data) to confirm the correct substring (`"initialize2"`) for Raydium-based token creation.  
- **Flexible Parsing**  
  - I used a helper function (`extract_contract_address`) to look for a `"mint"` in the `tokenBalances`. This function can be modified easily if the data structure changes.

---

## **4. Constraints & Limitations**

- **Reliance on Decoded Format**  
  - Our solution assumes the block is already **decoded** in a certain JSON structure. If the structure changes, or if logs are truncated, the script may fail or miss some tokens.
  - Also I was clear about the Raydium one but not about the generic SPL mint generation so I also added that as Ill.
- **Log-Dependent**  
  - I rely on the presence of `"initialize2"` or `"InitializeMint"` in the logs. If these logs are missing or changed by a custom program, our detection might miss tokens.  
- **Partial Extraction**  
  - Not all transactions may provide enough data in `tokenBalances` to yield the contract address. I handle this gracefully by printing `"Token Contract Address not found."`  

---

## **Conclusion**

The provided solution meets the **core requirement** of:

1. **Reading a JSON block** from storage.  
2. **Identifying transactions** that create new tokens (Raydium or generic SPL).  
3. **Printing the transaction signature** of those creation transactions.

Furthermore, I also demonstrate the **bonus** capabilities:

- Identifying **where** the Raydium program was executed by printing relevant invocation details.
- Attempting to extract the **new token’s contract address** (if present in `tokenBalances`).  
