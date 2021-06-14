from pydantic import BaseModel

class Waifu(BaseModel):
    favourites: int
    imageURL: str 
    name: str 
    sacrificed: int # 0 for alive, 1 for has been sacrificed

class User(BaseModel):
    name: str
    avatarURL: str
    totalValue: str
    userId: str