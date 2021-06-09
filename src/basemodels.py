from pydantic import BaseModel

class Waifu(BaseModel):
    favourites: int
    imageURL: str ='https://images-na.ssl-images-amazon.com/images/I/61iwElTo6ML.jpg'
    name: str = ''