import csv
from neo4j import GraphDatabase

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_movies(self):
        with self.driver.session() as session:
            with open('movies.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Skip the header row
                next(reader, None)
                for row in reader:
                    genres = row['genres'].split('|')
                    for genre in genres:
                        session.run("""
                            MERGE (movie:Movie {movieId: $movieId})
                            MERGE (g:Genre {name: $genre})
                            MERGE (movie)-[:IN_GENRE]->(g)
                            SET movie.title = $title
                        """, movieId=int(row['movieId']), title=row['title'], genre=genre)

    def load_ratings(self):
        with self.driver.session() as session:
            with open('ratings.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    session.run("""
                        MERGE (user:User {userId: $userId})
                        MERGE (movie:Movie {movieId: $movieId})
                        MERGE (user)-[:RATED {rating: $rating}]->(movie)
                    """, userId=int(row['userId']), movieId=int(row['movieId']), rating=float(row['rating']))

    ############ Step 1 definitions ############
    def get_user_id(self):
        return int(input("Enter your user ID (between 1 and 600): "))
    
    def get_user_info(self, userId):
        with self.driver.session() as session:
            result = session.run("""
                OPTIONAL MATCH (user:User {userId: $userId})
                RETURN user.username AS username, CASE WHEN user.username IS NOT NULL THEN true ELSE false END AS exists
            """, userId=userId)
            return result.single()
        
    def create_user(self, userId, username):
        with self.driver.session() as session:
            session.run("""
                MERGE (user:User {userId: $userId})
                SET user.username = $username
            """, userId=userId, username=username)
    ############ END Step 1 ############

    ############ Step 2 definitions ############
    def search_movies(self, keyword, userId):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (movie:Movie) 
                WHERE toLower(movie.title) CONTAINS toLower($keyword) 
                OPTIONAL MATCH (user:User)-[r:RATED]->(movie) 
                OPTIONAL MATCH (movie)-[:IN_GENRE]->(genre)
                WITH movie, COLLECT(DISTINCT genre.name) AS genres, 
                    AVG(r.rating) AS avg_rating, 
                    COUNT(r) > 0 AS seen, 
                    COALESCE(MAX(CASE WHEN user.userId = $userId THEN r.rating END), "N/A") AS user_rating
                RETURN movie.title AS title, genres, avg_rating, seen, user_rating
                ORDER BY title
            """, keyword=keyword, userId=userId)
            return [record.data() for record in result]
    
    def print_movie_details(self, keyword, userId):
        movies = self.search_movies(keyword, userId)

        if movies:
            print("\nMatching Movies:")
            for movie in movies:
                title = movie.get("title", "N/A")
                genres = movie.get("genres", [])  # Use get to handle potential missing key
                avg_rating = movie.get("avg_rating", "N/A")
                user_rating = movie.get("user_rating", "N/A")

                seen = user_rating != "N/A"
                
                print(f"\nTitle: {title}")
                if genres:
                    print(f"Genres: {', '.join(genres)}")  # Join genres into a comma-separated string
                else:
                    print("Genres: N/A")
                print(f"Average Rating: {avg_rating}")
                print(f"Seen: {seen}")
                if seen:
                    print(f"Your Rating: {user_rating}")
                else:
                    print(f"Your Rating: N/A")
        else:
            print("No matching movies found.")
    ############ END Step 2 ############

    ############ Step 3 definitions ############
    def get_recommendations(self, userId):
        with self.driver.session() as session:
            result = session.run("""
            // Specify user ID 
            WITH """ + str(userId) + """ AS X 

            // Find the genre with the highest preference for the specified user 
            MATCH (user:User {userId: X})-[:GENRE_PREF]->(genre:Genre) 
            WITH user, genre 

            // Order by preference in descending order and limit to 1 
            ORDER BY genre.preference DESC 
            LIMIT 1 

            // Collect movies already rated by the user 
            MATCH (user)-[:RATED]->(m:Movie) 
            WITH user, genre, COLLECT(m.title) AS ratedMovies 

            // Find recommended movies in the genre with the highest preference 
            MATCH (genre)<-[:IN_GENRE]-(recommendedMovie:Movie) 
            WHERE NOT recommendedMovie.title IN ratedMovies 

            // Filter recommended movies based on rating information
            WITH recommendedMovie 

            // Match ratings given to recommended movie by users
            MATCH(recommendedMovie)<-[r:RATED]-(:User)

            // Calculate average rating and count of ratings 
            WITH recommendedMovie,
                COALESCE(AVG(r.rating), 0) AS avg_rating,
                COUNT(r) AS num_ratings 
            
            // Filter movies with more than 10 ratings
            WHERE num_ratings > 10

            // Return recommended movies with calculated average rating and number of ratings 
            RETURN recommendedMovie.movieId AS movieId, recommendedMovie.title AS title, avg_rating, num_ratings
            ORDER BY avg_rating DESC, num_ratings DESC 
            LIMIT 5;
            """, userId=userId)

            recommendations = [record.data() for record in result]
            self.print_recommendations(recommendations)

    def print_recommendations(self, recommendations):
        if recommendations:
            print("\nTop 5 Recommendations:")
            for recommendation in recommendations:
                movie_id = recommendation.get("movieId", "N/A")
                title = recommendation.get("title", "N/A")
                avg_rating = recommendation.get("avg_rating", "N/A")
                num_ratings = recommendation.get("num_ratings", 0)

                print(f"\nMovie ID: {movie_id}")
                print(f"Title: {title}")
                print(f"Average Rating: {avg_rating}")
                print(f"Number of Ratings: {num_ratings}")
        else:
            print("No recommendations found.")
    ############ END Step 3 ############

    ############ Step 4 definitions ############
    def rate_movie(self, userId, movieId, rating):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (user:User {userId: $userId})
                MATCH (movie:Movie {movieId: $movieId})
                MERGE (user)-[r:RATED]->(movie)
                SET r.rating = $rating
            """, userId=userId, movieId=movieId, rating=rating)
            print(f"Rating {rating} for Movie ID {movieId} added successfully!")
    ############ END Step 4 ############

    def start(self):
        userId = self.get_user_id()

        user_info = self.get_user_info(userId)
        user_exists = user_info["exists"]
        username = user_info["username"]

        if user_exists and username:
            print(f"\nWelcome back, {username}!")
        else:
            if not user_exists:
                new_username = input(f"Enter a username for userID {userId}: ")
                self.create_user(userId, new_username)
                print(f"Username {new_username} has been added to the database.")
            else:
                print(f"Hello, {username}! Your name has been added to the database.")

        while True:
            self.print_menu()
            choice = int(input("Enter your choice (1-4): "))

            if choice == 4:
                break  # Exit the loop if the user chooses to exit

            self.execute_menu_choice(choice, userId)

        self.close() # Step 5 Close Connections 
        
    def print_menu(self):
        print("\nMenu:")
        print("1. Search for Movies")
        print("2. Get Recommendations")
        print("3. Rate a Movie")
        print("4. Exit")

    def execute_menu_choice(self, choice, userId):
        if choice == 1:
            search_keyword = input("Enter a keyword to search for movies: ")
            self.print_movie_details(search_keyword, userId)
        elif choice == 2:
            self.get_recommendations(userId)
        elif choice == 3:
            movie_id_to_rate = int(input("Enter the Movie ID to rate (0 if none): "))
            if movie_id_to_rate != 0:
                rating = float(input("Enter your rating (between 1 and 5): "))
                self.rate_movie(userId, movie_id_to_rate, rating)
        elif choice == 4:
            print("Exiting...")
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    greeter = App("bolt://localhost:7687", "neo4j", "***********")
    greeter.start()