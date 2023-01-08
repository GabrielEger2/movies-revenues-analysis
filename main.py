import requests
from bs4 import BeautifulSoup
import pandas as pd


# Using TMDB to find a movie director's id inside the API
api_key = "c36f9d4a781179b2302784e7119c481f"
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
movies = table.find_all('a', class_ = 'tooltip') # Finding all movies within the direct html table

# Creating the lists that are  going to be used in pandas
total_titles = []
total_dates = []
total_budgets = []
total_revenues = []

# Finding movies ids with the API and finding it's data with web scrapping
for movie in movies:
    try:
        movie_name = movie.getText().replace(' ', '%20')
        api_path = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_name}&page=1&include_adult=false'
        response = requests.get(url=api_path)
        data = response.json()
        data = data['results'][0]
        url = f"https://www.themoviedb.org/movie/{data['id']}-{data['title'].replace(' ', '-').lower()}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        left_column = soup.find_all('section', class_ = 'facts left_column')
        for section in left_column: # Getting the important data within the html left column
            budget = section.contents[7]
            budget = str(budget.text).replace('Budget ', '')
            revenue = section.contents[9]
            revenue = str(revenue.text).replace('Revenue ', '')
            title = data['title']
            release_date = data['release_date']

            # Appending the movie information to the lists
            total_titles.append(title)
            total_dates.append(release_date)
            total_budgets.append(budget)
            total_revenues.append(revenue)
    except:
        pass

# creating the dataframe with the lists
df = pd.DataFrame({
    "Title": total_titles,
    "Release Date": total_dates,
    "Budget": total_budgets,
    "Revenue": total_revenues
})

print(df)