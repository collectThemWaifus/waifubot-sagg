import requests
import json

def findWaifu(perpage):
  # Here we define our query as a multi-line string
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

  # Define our query variables and values that will be used in the query request
  variables = {
      'perpage': perpage
}

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  return(response.text)

x = json.loads(findWaifu(30))
print(x)