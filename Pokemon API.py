import requests
import pandas as pd

base_url = 'https://pokeapi.co/api/v2/'
endpoint = 'generation'
url_test = 'https://pokeapi.co/api/v2/generation/1/'
r = requests.get(base_url + endpoint)
url = r.json()['results'][0]['url']


def get_generation(response):
    all_data = []
    for item in response['results']:
            hi = item['url']
            data = requests.get(hi).json()
            all_data.append(data)
    return all_data

#return list of all region in terminal but not useable
# def get_generation1(response):
#     for item in response['results']:
#            hi = print(item['url'])
#     return 

def get_generation1(response):
    for item in response['results']:
           hi = item['url']

    return hi

print(requests.get(url_test).json()['pokemon_species'][0]['name'])

#get_region(url)

def get_region(response):
       regions = []
       for x in response:
           data = x['main_region']['name']
           regions.append(data)
       return regions


# def get_pokemon(response):
#       all_pokemon = []
#       for x in response:
#             pok = {
#                   'name' : x['pokemon_species'][0]['name'],
#                   'url' : x['pokemon_species'][0]['url']
#             }
#             all_pokemon.append(pok)
#             return all_pokemon



def get_pokemon(response):
    all_pokemon = []
    for generation_data in response:
        for species_data in generation_data['pokemon_species']:
            pokemon = {
                'name': species_data['name'],
                'url': species_data['url'],
                
            }
            all_pokemon.append(pokemon)
    return all_pokemon

            
# def get_region(response):
#     regions = []  # Create an empty list to store region names
#     for data in response:  # Iterate over each item in the response list
#         if 'main_region' in data:  # Check if the 'main_region' key exists in the current item
#             region_name = data['main_region']['name']  # Get the value associated with the 'name' key in the 'main_region' dictionary
#             if region_name:  # Check if the region name is not empty
#                 regions.append(region_name)  # Append the region name to the list of regions
#     return regions  # Return the list of region names





generation_websites = get_generation(requests.get(base_url + endpoint).json())
regions = get_region(generation_websites)
pokemon = get_pokemon(generation_websites)

df = pd.json_normalize(pokemon)

df.to_csv(r'G:\My Drive\Glencore\pokemon.csv')



#-- Next need to get dictionary of all the pokemon I want


#['moves'][0]['name']

#abilities
#pokemon species
#types





#def get_region(response):
#    list_gen_url = []
#    for item in response:
#        gen = {
#            'url': item['url']
#        }
#        list_gen_url.append(gen)
#    return list_gen_url


#r2 = requests.get(generations)
