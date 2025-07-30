from .database import BeamDatabase 
from .bank import Bank

class Database(BeamDatabase):
    """A database subclass that passes the database connection to other classes."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bank = Bank(self.db)
