from pydantic import BaseModel

class Waifu(BaseModel):
    female: bool
    age: int
    name: str = ''