from pydantic import BaseModel

class Waifu(BaseModel):
    favourites: int
    imageURL: str 
    name: str 