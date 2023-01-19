import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt

# Load Requirements
with open('requirements.txt') as f:
    requirements = f.readlines()

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
    "Release_Date": total_dates,
    "Budget": total_budgets,
    "Revenue": total_revenues
})
print(df.isna().values.any()) # checking for NaN cells
print(df.duplicated().values.any()) # checking for duplicated cells
df.to_excel('raw_data.xlsx')

# Remove rows with no budget or revenue
for ind in df.index:
    if df['Budget'][ind] == '-' or df['Revenue'][ind] == '-':
        df.drop(ind, axis = 0, inplace= True)

# Convert the budget and value data format by removing the $, . and , symbols
chars_to_remove = [',', '$',]
columns_to_clean = ['Budget', 'Revenue']
for col in columns_to_clean:
    for char in chars_to_remove:
        # Replace each character with an empty string
        df[col] = df[col].astype(str).str.replace(char, "")
    # Convert column to a numeric data type
    df[col] = pd.to_numeric(df[col])

df.to_excel('clean_data.xlsx')

# Convert date data type to a DataTime OBJ
df.Release_Date = pd.to_datetime(df.Release_Date)

# Finding the Budget x Revenue plot:
plt.figure(figsize=(8, 4), dpi=200)

with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=df,
                         x='Budget',
                         y='Revenue',
                         hue='Revenue',  # colour
                         size='Revenue', )  # dot size

    ax.set(ylim=(0, df['Revenue'].max(axis=0)*1.25),
           xlim=(0, df['Budget'].max(axis=0)*1.25),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions', )

plt.show()

# Finding the Time x Revenue plot:
with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=df,
                         x='Release_Date',
                         y='Revenue',
                         hue='Revenue',  # colour
                         size='Revenue', )  # dot size

    ax.set(ylim=(0, df['Revenue'].max(axis=0)*1.25),
           xlim=(df.Release_Date.min(), df.Release_Date.max()),
           ylabel='Revenue in $ billions',
           xlabel='Years', )

plt.show()

# Running a linear regression to analyse the relationship ship between budget and revenue
plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style('darkgrid'):
    ax = sns.regplot(data=df,
                     x='Budget',
                     y='Revenue',
                     color='#2f4b7c',
                     scatter_kws={'alpha': 0.3},
                     line_kws={'color': '#ff7c43'})

    ax.set(ylim=(0, df['Revenue'].max(axis=0)*1.25),
           xlim=(0, df['Budget'].max(axis=0)*1.25),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')

plt.show()
