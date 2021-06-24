from typing import List
import requests
import random
from basemodels import Waifu

def findWaifu(ammount : int,whichpage: int) -> List[Waifu]:

  query = '''
  query ($perpage: Int, $whichpage: Int) { # Define which variables will be used in the query (id) 
    Page(page: $whichpage, perPage: $perpage) { 
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
  variables = { 'perpage': ammount,'whichpage': whichpage }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  parsedJson = requests.post(url, json={'query': query, 'variables': variables}).json()

  #Create and return list of waifus
  listOfWaifu = []
  for character in parsedJson["data"]["Page"]['characters']:
    newWaifu = Waifu(imageURL=character["image"]["medium"], name=character["name"]["full"], favourites=character["favourites"])
    listOfWaifu.append(newWaifu)
  return listOfWaifu

def GetCasteWaifu(ranking): #page 67, threshold = 500 fav min
  if ranking == 'SSS': #top 20 - 1% (SSS): 27.8k - 12.2k favourites
    waifulist = findWaifu(20,1)
    return(waifulist[random.randrange(20)])

  if ranking == "SS":  #20-60th - 3% (SS) 12k - 8.2k favourites
    waifulist = findWaifu(20,2)
    waifulist = waifulist + findWaifu(20,3)
    return(waifulist[random.randrange(40)])

  if ranking == "S":  #60-120th - 8% (S) 8k - 5.4k favourites
    waifulist = []
    for x in range(4,7):
      waifulist = waifulist + findWaifu(20,x)
    return(waifulist[random.randrange(60)])
  
  if ranking == "A": #120-200th - 14% (A) 5.4k - 3.7k favourites 
    waifulist = []
    for x in range(7,11):
      waifulist = waifulist + findWaifu(20,x)
    return(waifulist[random.randrange(80)])

  if ranking == "B": #200-420th - 22% (B) 3.7k - 2k favourites
    waifulist = []
    for x in range(11,22):
      waifulist = waifulist + findWaifu(20,x)
    return(waifulist[random.randrange(220)])

  if ranking == "C": #420-820th - 31% (C) 2k - 934 favourites
    waifulist = []
    for x in range(22,42):
      waifulist = waifulist + findWaifu(20,x)
    return(waifulist[random.randrange(400)])

  if ranking == "D": #820-1320th - 37% (D) 935 - 525 favourites
    waifulist = [] 
    for x in range(42,67):
      waifulist = waifulist + findWaifu(20,x)
    return(random.randrange(500))

    








