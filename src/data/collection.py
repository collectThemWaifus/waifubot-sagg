from typing import List
import requests
import random
from data.basemodels import Waifu


def findWaifu(ammount: int, whichpage: int) -> List[Waifu]:

    query = '''
  query ($perpage: Int, $whichpage: Int) {
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
    variables = {'perpage': ammount, 'whichpage': whichpage}

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    parsedJson = requests.post(
        url, json={'query': query, 'variables': variables}).json()

    # Create and return list of waifus
    listOfWaifu = []
    for character in parsedJson["data"]["Page"]['characters']:
        newWaifu = Waifu(imageURL=character["image"]["medium"],
                         name=character["name"]["full"],
                         favourites=character["favourites"])
        listOfWaifu.append(newWaifu)
    return listOfWaifu


def GetCasteWaifu(ranking):  # page 67, threshold = 500 fav min
    match ranking:
        case 'SSS':  # top 20 - 1% (SSS): 28016 - 12324 favourites
            waifulist = findWaifu(20, 1)

        case "SS":  # 20-60th - 3% (SS) 12k - 8.2k favourites
            waifulist = findWaifu(20, 2)
            waifulist = waifulist + findWaifu(20, 3)

        case "S":  # 60-120th - 8% (S) 8k - 5.4k favourites
            waifulist = []
            x = random.randrange(4, 7)
            waifulist = waifulist + findWaifu(20, x)

        case "A":  # 120-200th - 14% (A) 5.4k - 3.7k favourites
            waifulist = []
            x = random.randrange(7, 11)
            waifulist = waifulist + findWaifu(20, x)

        case "B":  # 200-420th - 22% (B) 3.7k - 2k favourites
            waifulist = []
            x = random.randrange(11, 22)
            waifulist = waifulist + findWaifu(20, x)

        case "C":  # 420-820th - 31% (C) 2k - 934 favourites
            waifulist = []
            x = random.randrange(22, 42)
            waifulist = waifulist + findWaifu(20, x)

        case  "D":  # 820-1320th - 37% (D) 934 - 525 favourites
            waifulist = []
            x = random.randrange(42, 52)
            waifulist += findWaifu(20, x)
    return(waifulist[random.randrange(20)])