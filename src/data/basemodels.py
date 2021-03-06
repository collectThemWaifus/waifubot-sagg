from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: Optional[str]
    avatarURL: Optional[str]
    totalValue: int
    userId: str
    serverid: Optional[str]

class Waifu(BaseModel):
    favourites: int
    imageURL: str
    name: str
    sacrificed: int = 0  # 0 for alive, 1 for has been sacrificed
    claimerId: Optional[str]
    claimerUser: Optional[User]
    serverid: Optional[str]