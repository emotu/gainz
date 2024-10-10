from datetime import datetime, timezone

from beanie import Document
from pydantic import Field

AutoDateTime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SavedAssistant(Document):
    """
    OpenAI Assistant Model to map assistants to individual users after they are logged in
    """

    assistant_id: str
    user_id: str


class SavedThread(Document):
    """
    OpenAI Thread Model to map threads to individual users after they are logged in, so the data can be retrieved
    """
    thread_id: str
    user_id: str
