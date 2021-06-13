from pydantic import BaseModel

class Waifu(BaseModel):
    favourites: int
    imageURL: str 
    name: str 

class User(BaseModel):
    name: str
    avatarURL: str
    totalValue: str
    userId: str