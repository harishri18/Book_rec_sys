import pandas as pd


books = pd.read_csv('/home/pratik/Downloads/Books.csv')
user = pd.read_csv('/home/pratik/Downloads/Users.csv')
ratings = pd.read_csv('/home/pratik/Downloads/Ratings.csv')

# Merge ratings with users
ratings_users = pd.merge(ratings, user, on='User-ID')

# Merge the result with books
merged_df = pd.merge(ratings_users, books, on='ISBN')
df = merged_df.copy()