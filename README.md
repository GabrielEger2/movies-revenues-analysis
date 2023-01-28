# Movies Revenues Analysis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
This is a code repository for an analyser of movies revenues from inputted directors, that uses Pandas, Seaborn, and Beautiful soup

<h3>Requirements</h3>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
In order to locally use this program, you must install the libraries requirements using the following command: 

```bash
 pip install -r requirements.txt
```
    
<h3>Environment Variables</h3>

This project uses the TMDB API that, although free to use, requires a user key

`api_key` = "API KEY"

<h3>Expected Output</h3>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Once the code is initialized, an input asking for the name of a director will appear; in this example we will use Steven Spielberg

![github_movie ](https://user-images.githubusercontent.com/52424334/213895942-8c371e13-de25-4828-8988-4d999c8d3ca0.png)

(The director's name must be within The Movie DataBase (TMDB) Website)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
After that, the code will search for every movie from that director inside the TMDB website and its respective dates, names, budgets and revenues, cleaning all the invalid data in the process

![github_movie5](https://user-images.githubusercontent.com/52424334/213895969-3a0ec592-5700-4c82-b901-e4602d52b445.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Finally, the code will show three charts made with seaborn showing the revenue over budget, revenue over time, and a linear regression of the revenue over budget

![github_movie2](https://user-images.githubusercontent.com/52424334/213895987-a21d0b40-9aa5-47e6-bbe8-322b1e78b664.png)

![github_movie3](https://user-images.githubusercontent.com/52424334/213896005-e061ffd9-f099-4c70-b1e0-537a9c99435f.png)

![github_movie4](https://user-images.githubusercontent.com/52424334/213896020-50d0d5e5-e757-43bd-9ee4-1317e82a816e.png)


