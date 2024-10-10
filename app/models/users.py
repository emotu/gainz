from datetime import datetime, timezone
from typing import Optional, Annotated

import bcrypt
from beanie import Document, Indexed
from pydantic import Field, ConfigDict, SecretStr

AutoDateTime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(Document):
    """
    Model to store and attribute models to
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Optional[str] = None

    username: Annotated[str, Indexed(unique=True)]
    password: Annotated[str | SecretStr | None, Field(exclude=True)] = None

    date_created: datetime = AutoDateTime
    last_updated: datetime = AutoDateTime

    def set_password(self, password: str | bytes):
        """
        Internal method to set a password on a user before saving the user to the database.
        @param password: new password to be set
        @return: User object
        """
        self.password = (bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())).decode()

    def check_password(self, password) -> bool:
        """
        Check the password of the against the existing password in the database

        @param password: password to compare against
        @return: bool
        """

        if not password or not isinstance(password, (str, bytes)):
            raise ValueError("Password must be non-empty string or bytes value")
        password = password.encode('utf-8')

        # both password and hashed password need to be encrypted.
        return bcrypt.checkpw(password, self.password.encode('utf-8'))

    @classmethod
    async def check_user_exists(cls, username: str) -> "User":
        """
        @param username: Username address to check

        @return: exists (True|False)
        """

        return await cls.find_one(
            cls.username == username
        )