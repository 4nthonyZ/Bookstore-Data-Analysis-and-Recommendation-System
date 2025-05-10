import pandas as pd
from helpers.file_io import create_csv
from helpers.data_processing import get_author_books

def get_average_rating_from_author(df_books, df_ratings, author):
    # Filter df by author
    df_author = get_author_books(df_books, author)
    
    # Get ratings of author books
    # Use the ISBNs from df_author to filter df_ratings
    isbns = df_author['ISBN'].unique()
    df_ratings_author = df_ratings[df_ratings['ISBN'].isin(isbns)]
    
    # Calculate the average rating for these ISBNs
    if not df_ratings_author.empty:
        average_rating = df_ratings_author['Book-Rating'].mean()
    else:
        average_rating = None  # or return an appropriate message or value indicating no ratings found
    
    return average_rating

def get_average_ratings_all_authors(df_books, df_ratings):
    # Merge books and ratings data on ISBN
    df_merged = pd.merge(df_books[['ISBN', 'Book-Author']], df_ratings[['ISBN', 'Book-Rating']], on='ISBN')
    df_author_ratings = df_merged.groupby('Book-Author').agg(
        AverageRating=('Book-Rating', 'mean'),
        TotalRatings=('Book-Rating', 'count')
    ).reset_index()
    return df_author_ratings

def combine_author_data(df_books, df_author_ratings):
    # Count books per author
    df_author_counts = df_books['Book-Author'].value_counts().reset_index()
    df_author_counts.columns = ['Book-Author', 'Book-Count']

    # Merge with average ratings
    df_author_info = pd.merge(df_author_counts, df_author_ratings, on='Book-Author', how='left')
    return df_author_info

def main(df_books, df_ratings):
    df_author_ratings = get_average_ratings_all_authors(df_books, df_ratings)
    df_author_info = combine_author_data(df_books, df_author_ratings)
    create_csv(df_author_info, "output/AuthorInfo.csv")
    return df_author_info

if __name__ == "__main__":
    main()