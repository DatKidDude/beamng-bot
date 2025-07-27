import pymongo
import asyncio
from datetime import datetime, timezone
from pymongo.asynchronous.database import AsyncDatabase
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

    
    async def add_account(self, discord_member):
        collection = self._conn["bank"]
        await collection.update_one(
            {"discord_id": discord_member["discord_id"]},
            {"$set": {"username": discord_member["username"],
                      "currency": discord_member["currency"],
                      "created_at": datetime.now(tz=timezone.utc)
                      }},
            upsert=True
        )

    # update balance
    async def update_balance(self, amount: int):
        pass

    # get balance
    async def get_balance(self):
        pass

    # spend currency
    async def spend_currency(self):
        pass
