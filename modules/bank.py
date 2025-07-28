import pymongo
import asyncio
from datetime import datetime, timezone
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.typings import _DocumentType
from typing import Any, Dict
from database import BeamDatabase

class Bank:
    TABLE_NAME = "bank"

    def __init__(self, db: AsyncDatabase) -> None:
        """Initializes an async instance of the BeamDatabase class
        
        Args:
            db (AsyncDatabase): Pymongo AsyncDatabase instance
        """
        self._conn = db # connection to the database instance
    
    # create table if not exists
    async def create_table(self):
        """
        Creates a 'bank' collection if one does not exists and then creates
        a discord_id index
        """
        tables = await self._conn.list_collection_names()
        if Bank.TABLE_NAME not in tables:
            print("Creating 'bank' table")
            table = await self._conn.create_collection(Bank.TABLE_NAME) # create the table
            print("Creating index")
            await table.create_index([("discord_id")], unique=True) # create index in ascending order

    
    async def add_account(self, discord_member: Dict[str, Any]):
        """
        Adds a user to the bank collection

        Args:
            discord_member (Dict[str, Any]): Document object to be added to the collection
        """
        collection = self._conn[Bank.TABLE_NAME]
        await collection.update_one(
            {"discord_id": discord_member["discord_id"]},
            {"$set": {"username": discord_member["username"],
                      "currency": discord_member["currency"],
                      "created_at": discord_member["created_at"]
                      }},
            upsert=True)

    async def get_balance(self, discord_id: str) -> str | None:
        """
        Returns the current balance of a user

        Args:
            discord_id (str): Discord_id of the user
        
        Returns:
            str | None: the current balance of the user
        """
        # find the user by discord_id
        user = await self._conn[Bank.TABLE_NAME].find_one({"discord_id": discord_id})
        
        # return the user's balance
        return user["currency"] if user else None

    async def update_balance(self, discord_id: str, amount: int, op: str):
        """
        Adds or subtracts the amount from the current balance

        Args:
            discord_id (str): Discord_id of the user 
            amount     (int): The amount to add or subtract
            op         (str): Addition or subtraction operator
        """
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

