import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
except OSError as e:
    print("Could not find .env file. Shutting down bot...")

@dataclass(frozen=True)
class Auth:
    """A dataclass to store .env variables"""
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DB_NAME: str = os.getenv("DB_NAME", "BeamDB")
    COMMAND_PREFIX: str = "!"