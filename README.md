# Use the following command to run the program specific to your computer

/usr/local/bin/python3.10 /Users/tommysubaric/mdb_hw8/setup.py

# Upon running the setup.py file the user will be prompted to Enter their user ID.

Enter your user ID (between 1 and 600): 

# If the User does not have a name property it will ask the user to add their name which will be added to the Database.

Enter your user ID (between 1 and 600): 5
Enter a username for userID 5: Guadalupe
Username Guadalupe has been added to the database.

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 

# If the User already has a name property it will welcome the User by their name back to the Movie Menu.

Enter your user ID (between 1 and 600): 1

Welcome back, Tommy!

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 

# Once inside the Movie Menu, the User can search for movies inside the IMDB based on keywords in the title. It will return the matching titles, the average rating of the film among all users. As well as if the logged in user has rated that specific movie or not. 

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 1     
Enter a keyword to search for movies: Django

Matching Movies:

Title: Django Unchained 
Genres: Action, Western, Drama
Average Rating: 3.9583333333333335
Seen: True
Your Rating: 5.0

Title: Sukiyaki Western Django 
Genres: Action, Western
Average Rating: 3.3333333333333335
Seen: False
Your Rating: N/A

# The User can get 5 movie recommendations of films that they have not rated based off of the movies that the user has already rated. 

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 2             

Top 5 Recommendations:

Movie ID: 1199
Title: Brazil 
Average Rating: 4.1779661016949134
Number of Ratings: 59

Movie ID: 741
Title: Ghost in the Shell (Kôkaku kidôtai) 
Average Rating: 4.148148148148149
Number of Ratings: 27

Movie ID: 3503
Title: Solaris (Solyaris) 
Average Rating: 4.090909090909091
Number of Ratings: 11

Movie ID: 1223
Title: Grand Day Out with Wallace and Gromit, A 
Average Rating: 4.089285714285714
Number of Ratings: 28

Movie ID: 6350
Title: Laputa: Castle in the Sky (Tenkû no shiro Rapyuta) 
Average Rating: 4.062499999999999
Number of Ratings: 24

# The User can also rate movies out of 5 stars.

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 3
Enter the Movie ID to rate (0 if none): 6350
Enter your rating (between 1 and 5): 3.5
Rating 3.5 for Movie ID 6350 added successfully!

# After the User rates the movie it will be replaced in the recommended movies

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 2

Top 5 Recommendations:

Movie ID: 1199
Title: Brazil 
Average Rating: 4.1779661016949134
Number of Ratings: 59

Movie ID: 741
Title: Ghost in the Shell (Kôkaku kidôtai) 
Average Rating: 4.148148148148149
Number of Ratings: 27

Movie ID: 3503
Title: Solaris (Solyaris) 
Average Rating: 4.090909090909091
Number of Ratings: 11

Movie ID: 1223
Title: Grand Day Out with Wallace and Gromit, A 
Average Rating: 4.089285714285714
Number of Ratings: 28

Movie ID: 60069
Title: WALL·E 
Average Rating: 4.057692307692307
Number of Ratings: 104

# Also when it is searched it will show that the user has seen the movie along with the rating given by the user. 

Menu:
1. Search for Movies
2. Get Recommendations
3. Rate a Movie
4. Exit
Enter your choice (1-4): 1
Enter a keyword to search for movies: Laputa

Matching Movies:

Title: Laputa: Castle in the Sky (Tenkû no shiro Rapyuta) 
Genres: Action, Animation, Fantasy, Children, Sci-Fi, Adventure
Average Rating: 4.04
Seen: True
Your Rating: 3.5

# When the User enters 4/'Exit' the connection between the Database will close