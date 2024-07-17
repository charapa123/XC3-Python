import requests
import pandas as pd

base_url = 'https://pokeapi.co/api/v2/'
endpoint = 'generation'

def get_generation(response):
    all_data = []
    all_data2 = []
    for item in response['results']:
        hi = item['url']
        data = requests.get(hi).json()
        all_data.append(data)
        all_data2.append(hi)
    return all_data, all_data2

#so this is just the data = all_data and url = all_data2, they just act as parameters
def get_pokemon(data_array, url_array):
    all_pokemon = []
    for generation_data, generation_url in zip(data_array, url_array):
        for species_data in generation_data['pokemon_species']:
            pokemon = {
                'name': species_data['name'],
                'url': species_data['url'],
                'generation_url': generation_url  # Add the generation URL to the Pokemon data
            }
            all_pokemon.append(pokemon)
    return all_pokemon

# Make the initial request and get the JSON data
response = requests.get(base_url + endpoint).json()

# Call get_generation with the JSON data
all_data, all_data2 = get_generation(response)

# Use the data returned by get_generation to get the Pokemon data
all_pokemon = get_pokemon(all_data, all_data2)

df = pd.json_normalize(all_pokemon)

df.to_csv(r'G:\My Drive\Glencore\pokemon_withcorrecturlidkhow.csv')



