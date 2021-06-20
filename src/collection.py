from typing import List
import requests
from basemodels import Waifu

def findWaifu(ammount : int) -> List[Waifu]:

  query = '''
  query ($perpage: Int) { # Define which variables will be used in the query (id) 
    Page(page: 50, perPage: $perpage) { 
       characters(sort: FAVOURITES_DESC){
          image{
            medium
          }
          favourites
          name {
            full
            
          }
        }
      }
    } 

  '''
  variables = { 'perpage': ammount }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  parsedJson = requests.post(url, json={'query': query, 'variables': variables}).json()

  #Create and return list of waifus
  listOfWaifu = []
  for character in parsedJson["data"]["Page"]['characters']:
    newWaifu = Waifu(imageURL=character["image"]["medium"], name=character["name"]["full"], favourites=character["favourites"])
    listOfWaifu.append(newWaifu)
  return listOfWaifu
