import requests
from bs4 import BeautifulSoup

# Using TMDB to find a movie director's id inside the API
api_key = "API KEY"
director = input('Please say the name of a movie director: ').replace(' ', '%20') #asking the director from an input
api_path = f'https://api.themoviedb.org/3/search/person?api_key={api_key}&language=en-US&query={director}&page=1&include_adult=false'

# Getting the director's id from a json file
response = requests.get(url=api_path)
data = response.json()
data = data['results'][0]

# Creating a list for the movies that the director made
# I've tried to find a method within the API to find all the movies directed by the director, but I couldn't
# So I just web scrapped the main page
movies_collected = []
url = f"https://www.themoviedb.org/person/{data['id']}-{data['name'].replace(' ', '-').lower()}"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all('table', class_ = 'card credits')
table = tables[0]
movies = table.find_all('a', class_ = 'tooltip')
for movie in movies:
    movies_collected.append(movie.getText()) # Appending all movies to the list
