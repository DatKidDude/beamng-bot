from .database import BeamDatabase 
from .bank import Bank

class Database(BeamDatabase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bank = Bank(self.db)
