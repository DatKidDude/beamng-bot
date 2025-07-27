import pymongo
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection

class BeamDatabase:
    
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self._conn = AsyncMongoClient()
    
    @property
    def db(self) -> AsyncDatabase:
        """
        Returns an Asynchronous MongoDB database instance
        
        Returns:
            AsyncDatabase: Asynchronous MongoDB database instance
        """
        return self._conn[self.db_name]
    
    def cursor(self, table_name: str) -> AsyncCollection:
        """
        Returns a MongoDB collection specified by the user

        Returns:
            AsyncCollection: A database table
        """
        return self.db[table_name]

