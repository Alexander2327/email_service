from pydantic import BaseModel


class UserMessageBody(BaseModel):
    message: str
    user_email: str
    subject: str