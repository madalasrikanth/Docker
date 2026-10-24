
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Banking Management System")

# Demo data only; use a database in the complete project.
accounts = {
    1001: {"name": "Arun", "balance": 5000.0}
}


class Transaction(BaseModel):
    amount: float


@app.get("/")
def home():
    return {"message": "Banking Management System API"}


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    account = accounts.get(account_id)

    if account is None:
        raise HTTPException(404, "Account not found")

    return account


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, transaction: Transaction):
    if account_id not in accounts:
        raise HTTPException(404, "Account not found")

    if transaction.amount <= 0:
        raise HTTPException(400, "Amount must be positive")

    accounts[account_id]["balance"] += transaction.amount
    return {"message": "Deposit successful",
            "balance": accounts[account_id]["balance"]}


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, transaction: Transaction):
    if account_id not in accounts:
        raise HTTPException(404, "Account not found")

    if transaction.amount <= 0:
        raise HTTPException(400, "Amount must be positive")

    if transaction.amount > accounts[account_id]["balance"]:
        raise HTTPException(400, "Insufficient balance")

    accounts[account_id]["balance"] -= transaction.amount
    return {"message": "Withdrawal successful",
            "balance": accounts[account_id]["balance"]}
