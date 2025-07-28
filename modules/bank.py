import pymongo
import asyncio
from datetime import datetime, timezone
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.typings import _DocumentType
from typing import Any, Dict
from database import BeamDatabase

class Bank:
    TABLE_NAME = "bank"

    def __init__(self, db: AsyncDatabase):
        self._conn = db # connection to the database instance
    
    # create table if not exists
    async def create_table(self):
        tables = await self._conn.list_collection_names()
        if Bank.TABLE_NAME not in tables:
            print("Creating 'bank' table")
            table = await self._conn.create_collection(Bank.TABLE_NAME) # create the table
            print("Creating index")
            await table.create_index([("discord_id")], unique=True) # create index in ascending order

    
    async def add_account(self, discord_member: Dict[str, Any]):
        collection = self._conn[Bank.TABLE_NAME]
        await collection.update_one(
            {"discord_id": discord_member["discord_id"]},
            {"$set": {"username": discord_member["username"],
                      "currency": discord_member["currency"],
                      "created_at": discord_member["created_at"]
                      }},
            upsert=True)

    async def get_balance(self, discord_id: str) -> str | None:
        # find the user by discord_id
        user = await self._conn[Bank.TABLE_NAME].find_one({"discord_id": discord_id})
        # return the user's balance
        return user["currency"] if user else None

    async def update_balance(self, discord_id: str, amount: int, op: str):
        balance_str = await self.get_balance(discord_id)
        
        if balance_str is None:
            raise ValueError("NoneType returned from get_balance()")
        
        new_balance = int(balance_str)
        if op == "+":
            new_balance += amount
        elif op == "-":
            new_balance -= amount
        else:
            raise ValueError("Invalid Operation")
        
        await self._conn[Bank.TABLE_NAME].update_one(
            {"discord_id": discord_id},
            {"$set": {"currency": str(new_balance)}}
        )
        

bdb = BeamDatabase("BeamDB")
bank = Bank(bdb.db)

async def main():
    account = {
        "discord_id": "837465013",
        "username": "datkiddude",
        "currency": "1000",
        "created_at": datetime.now(tz=timezone.utc).replace(microsecond=0),
    }
    # await bank.add_account(account)
    # currency = await bank.get_balance(account["discord_id"])
    await bank.update_balance(account["discord_id"], amount=200, op="+")
  
asyncio.run(main())

