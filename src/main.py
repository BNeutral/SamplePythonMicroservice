'''
Sample microservice to show some minimal skills.
'''
import sqlite3
import time
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from currencies import Currency, currency_decimals
from operations import Operation
from database import *

app = FastAPI()

class UserPersonalData(BaseModel):
    names: str
    surnames: str
    alias: str
    email: str

class UserTransactionData(BaseModel):
    uuid: int
    operation : Operation
    currency : Currency
    amount: int

@app.on_event("startup")
def startup_event():
    db_init()

@app.post("/users")
def user_new(userData: UserPersonalData):
    '''
    Creates a new user and persists in the DB
    '''
    #TODO: Validation, async, error handling, etc
    uuid = uuid4().int & 0xFFFFFFFFFFFF # Current DB only supports 8 bytes ints as max, so
    db_connection = db_get_connection()
    try:
        db_cursor = db_connection.cursor()
        db_cursor.execute('BEGIN TRANSACTION;')
        db_cursor.execute('INSERT INTO users(uuid,names,surnames,alias,email) VALUES(?,?,?,?,?)',
            (uuid, userData.names, userData.surnames, userData.alias, userData.email))
        for cur in Currency:
            db_cursor.execute('INSERT INTO '+db_balance_table_name(cur)+'(uuid,balance) VALUES(?,?)',(uuid,0))
        db_connection.commit()
        print(f"Created user {uuid}") #TODO: Proper logs
        return {}
    except sqlite3.IntegrityError as e:
        print(e) #TODO: Proper logs
        raise HTTPException(status_code=409, detail="Email or alias is already in use.")    
    finally:
        db_return_connetion(db_connection)


@app.get("/users/{uuid}")
def user_get(uuid: int):
    '''
    Returns the information for the user by uuid
    '''
    db_connection = db_get_connection()
    entry = db_connection.execute('SELECT names,surnames,alias,email FROM users WHERE uuid = ?', (uuid,)).fetchone()
    balances = get_user_balances(uuid, db_connection)
    db_return_connetion(db_connection)
    if entry is None:
        raise HTTPException(status_code=404, detail="User uuid not found")
    return {
        "names" : entry[0],
        "surnames" : entry[1],
        "alias" : entry[2],
        "email" : entry[3],
        "balances" : balances
    }

@app.post("/users/transaction/new")
def user_transaction_new(data: UserTransactionData):
    '''
    Performs a transaction on the user balances, according to the operation type.
    The amount is always a positive.
    Deposits increase the balance.
    Withdrawals decrease the balance, but the amount can't be greater than the balance.
    '''    
    if (data.amount <= 0):
        raise HTTPException(status_code=400, detail="Amounts should always be >= 0")
    db_connection = db_get_connection()
    try:
        db_cursor = db_connection.cursor()
        db_cursor.execute('BEGIN TRANSACTION;')

        #TODO: Double check our server timestamps are never desyncd, etc
        db_cursor.execute('INSERT INTO transactions(uuid,timestamp,operation,currency,amount) VALUES(?,?,?,?,?)',
            (data.uuid, int(time.time()), data.operation, data.currency, data.amount))

        amount = data.amount
        if (data.operation == Operation.withdraw):
            amount = -amount
        db_cursor.execute(f'UPDATE {db_balance_table_name(data.currency)} SET balance=balance+? WHERE uuid=(?)',(amount,data.uuid))
        db_connection.commit()
        return {}
    except sqlite3.IntegrityError as e:
        print(e) #TODO: Proper logs
        raise HTTPException(status_code=409, detail="Trying to remove more balance than the user has.")    
    finally:
        db_return_connetion(db_connection)

@app.get("/users/transaction/list")
def user_transaction_list(uuid: int, operation : Optional[Operation] = None, currency : Optional[Currency] = None, limit: int = 10, offset: int = 0):
    '''
    Gets a transaction history
    '''    
    db_connection = db_get_connection()

    op = "" if operation is None else f"AND operation = {operation.value} "
    cur = "" if currency is None else f"AND currency = {currency.value} "  
    entries = db_connection.execute(f'SELECT timestamp,operation,currency,amount FROM transactions\
        WHERE uuid = ? {op}{cur}LIMIT ? OFFSET ?;',
        (uuid,limit,offset))

    fetched = entries.fetchall()
    #TODO: Maybe add a check for id the uuid doesn't exist. This one tramples on a real use case.
    #if len(fetched) <= 0:
    #    db_return_connetion(db_connection)
    #    raise HTTPException(status_code=404, detail="No transactions found for this user.")
        
    results = []
    for entry in fetched:
        results.append({
            "timestamp" : entry[0],
            "operation" : Operation(entry[1]).name,
            "currency" : Currency(entry[2]).name,
            "amount" : entry[3],
        })
    db_return_connetion(db_connection)
    return { "transactions" : results }

def get_user_balances(uuid: int, db_connection : sqlite3.Connection):
    '''
    Returns all the balances of a user in list
    Receives a db connection that it doesn't close. Only performs reads on it.
    '''
    balances = []
    for cur in Currency:
        balances.append(get_user_balance(uuid, cur, db_connection))
    return balances

def get_user_balance(uuid: int, currency : Currency, db_connection : sqlite3.Connection):
    '''
    Returns the balance of a user for a particular currency.
    Receives a db connection that it doesn't close. Only performs reads on it.
    '''
    table_name = db_balance_table_name(currency)
    entry = db_connection.execute('SELECT balance FROM '+table_name+' WHERE uuid = ?', (uuid,)).fetchone()
    if entry is None:
        raise HTTPException(status_code=404, detail=f"User uuid not found for {currency.name}")
    return { 
        "currency" : currency.name,
        "decimals" : currency_decimals[currency],
        "balance" : entry[0]
    }

