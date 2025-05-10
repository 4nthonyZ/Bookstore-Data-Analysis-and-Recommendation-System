import pandas as pd
from helpers.file_io import create_csv

def get_books_info(df_books, df_ratings):
    df_merged = pd.merge(df_books, df_ratings, 'inner', 'ISBN')
    df_book_info = df_merged.groupby('ISBN').agg({
        'Book-Rating': ['mean', 'max', 'min', 'count']
    }).reset_index()
    df_book_info.columns = ['ISBN', 'Average Rating', 'Highest Rating', 'Lowest Rating', 'Number of Ratings']
    return df_book_info

def get_location_info(df_ratings, df_users):
    # Merge the ratings and users dataframes on 'User-ID'
    df_merged = pd.merge(df_ratings, df_users, on='User-ID', how='inner')
    
    # Group by location and ISBN
    grouped = df_merged.groupby(['User-City', 'User-State', 'User-Country', 'ISBN'])

    # Calculate average rating and count of ratings per book
    aggregated = grouped.agg({
        'Book-Rating': ['mean', 'count']
    }).reset_index()

    # Rename multi-level columns
    aggregated.columns = ['User-City', 'User-State', 'User-Country', 'ISBN', 'Average Rating', 'Number of Ratings']

    # Function to find the highest average rating and most popular book and combine them in one row
    def get_top_books(group):
        highest_rated = group.loc[group['Average Rating'].idxmax()]
        most_popular = group.loc[group['Number of Ratings'].idxmax()]
        return pd.Series({
            'Highest Rated ISBN': highest_rated['ISBN'],
            'Highest Rating': highest_rated['Average Rating'],
            'Most Popular ISBN': most_popular['ISBN'],
            'Most Ratings': most_popular['Number of Ratings']
        })

    # Apply the function to each group of city, state, country
    result = aggregated.groupby(['User-City', 'User-State', 'User-Country']).apply(get_top_books).reset_index()
    return result

def main(df_books, df_ratings, df_users):
    df_book_info = get_books_info(df_books, df_ratings)
    df_book_info = pd.merge(df_books, df_book_info, 'inner', 'ISBN')
    df_location_info = get_location_info(df_ratings, df_users)
    create_csv(df_book_info, "output/BookInfo.csv")
    create_csv(df_location_info, "output/LocationInfo.csv")
    return df_book_info, df_location_info

if __name__ == "__main__":
    main()