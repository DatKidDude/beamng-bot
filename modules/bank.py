import pymongo
import asyncio
from datetime import datetime, timezone
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.typings import _DocumentType
from typing import Any, Dict, Optional

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
        result = await collection.update_one(
            {"discord_id": discord_member["discord_id"]},
            {"$set": {"username": discord_member["username"],
                      "currency": discord_member["currency"],
                      "created_at": datetime.now(tz=timezone.utc),
                      "daily_cd": None,
                      "weekly_cd": None
                      }},
            upsert=True)
        return result
    
    async def get_account(self, discord_id: str):
        user: Optional[Dict[str, Any]] = await self._conn[Bank.TABLE_NAME].find_one({"discord_id": discord_id})

        if user is None:
            raise ValueError(f"NoneType returned in {self.get_account.__name__}")
        
        return user
    
    async def get_balance(self, discord_id: str) -> int:
        """
        Returns the current balance of a user

        Args:
            discord_id (str): Discord_id of the user
        
        Returns:
            str: The current balance of the user
        
        Raises:
            ValueError: Raises if user evaluates to None
        """
        
        user: Optional[Dict[str, Any]] = await self._conn[Bank.TABLE_NAME].find_one({"discord_id": discord_id})
        
        if user is None:
            raise ValueError(f"NoneType returned in {self.get_balance.__name__}")
    
        return user["currency"]

    async def update_balance(self, discord_id: str, amount: int, cooldown_field: Optional[str] = None, cooldown_time: Optional[str] = None) -> int:
        """
        Adds or subtracts the amount from the current balance.
        If cooldown_date is passed that means the user was able to use
        the daily or weekly command.

        Args:
            discord_id (str): Discord_id of the user 
            amount     (int): The amount to add or subtract
            cooldown_date (datetime): The next time the user can use the daily or weekly command
        """
        set_update: Dict[str, Any] = {"$inc": {"currency": amount}}

        # updates the daily or weekly cooldown time
        if cooldown_field and cooldown_time:
            set_update.setdefault("$set", {})[cooldown_field] = cooldown_time
        
        await self._conn[Bank.TABLE_NAME].update_one(
            {"discord_id": discord_id},
            update=set_update
            )
        
        return await self.get_balance(discord_id=discord_id)
        

    async def check_user_exists(self, discord_id: str) -> bool:
        """Verifies if a user exists in the database by their discord id"""
        user = await self._conn[Bank.TABLE_NAME].find_one({"discord_id": discord_id})
        return True if user else False
        

