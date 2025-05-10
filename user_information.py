import pandas as pd
from helpers.file_io import create_csv
from helpers.data_processing import merge_df

def get_highest_ratings(df_books, df_ratings):
    # Find the maximum rating for each user
    df_highest_ratings = df_ratings.groupby('User-ID')['Book-Rating'].max().reset_index(name='Highest-Rating')
    
    # Merge the highest ratings with original ratings to find all the books that received this rating
    df_highest_rated_books = pd.merge(df_highest_ratings, df_ratings, on='User-ID', how='inner')
    
    # Merge with books data to get book titles
    df_highest_rated_books = pd.merge(df_highest_rated_books, df_books[['ISBN', 'Book-Title']], on='ISBN', how='left')
    
    # Ensure column name consistency when grouping and aggregating
    df_highest_rated_books = df_highest_rated_books.groupby('User-ID').agg({
        'Book-Title': 'first',
        'Highest-Rating': 'first'
    }).reset_index()
    df_highest_rated_books.columns = ['User-ID', 'Favourite-Books', 'Highest-Rating']
    
    return df_highest_rated_books

def get_favourite_author(df_books, df_ratings):
    # Merge ratings with books data to include author information
    df_ratings_with_authors = pd.merge(df_ratings, df_books[['ISBN', 'Book-Author']], on='ISBN', how='left')
    
    # Calculate the average rating for each author per user
    df_author_ratings = df_ratings_with_authors.groupby(['User-ID', 'Book-Author'])['Book-Rating'].mean().reset_index(name='Average-Author-Rating')
    
    # Find the highest average rating per user
    df_max_author_ratings = df_author_ratings.groupby('User-ID')['Average-Author-Rating'].max().reset_index(name='Highest-Author-Rating')
    
    # Merge back to get the author(s) with the highest average rating per user
    df_favourite_authors = pd.merge(df_max_author_ratings, df_author_ratings, on='User-ID', how='inner')
    
    # Reduce to one entry per user in case of ties (taking the first one)
    df_favourite_authors = df_favourite_authors.drop_duplicates(subset=['User-ID'])
    
    # Select relevant columns and rename for clarity
    df_favourite_authors = df_favourite_authors[['User-ID', 'Book-Author']].rename(columns={'Book-Author': 'Favourite-Author'})
    
    return df_favourite_authors


def main(df_books, df_ratings, df_users):
    # Get user average rating
    df_user_avg_rating = df_ratings.groupby('User-ID')['Book-Rating'].mean().reset_index(name='Average-Rating')
    # Create user info dataframe and append average rating
    df_user_info = merge_df(df_users, df_user_avg_rating, "inner", "User-ID")

    # Get user number of ratings
    df_user_number_ratings = df_ratings['User-ID'].value_counts().reset_index()
    df_user_number_ratings.columns = ['User-ID', 'Count']
    # Append number of ratings
    df_user_info = merge_df(df_user_info, df_user_number_ratings, "inner", "User-ID")

    # Get favourite books
    df_highest_ratings = get_highest_ratings(df_books, df_ratings)
    df_user_info = merge_df(df_user_info, df_highest_ratings, "inner", "User-ID")
    
    # Get favourite author and append to user info
    df_favourite_author = get_favourite_author(df_books, df_ratings)
    df_user_info = merge_df(df_user_info, df_favourite_author, "inner", "User-ID")    
    create_csv(df_user_info, "output/UserInfo.csv")
    return df_user_info

if __name__ == "__main__":
    main()