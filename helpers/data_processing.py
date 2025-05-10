import pandas as pd

## Data information
def get_df_length(df):
    # Returns the length of a given dataframe
    return df.shape[0]

def get_df_columns(df):
    # Returns column names as a list
    columns = df.columns.values.tolist()
    return columns

##  Merge df
def merge_df(df1, df2, how, on):
    df = df1.merge(df2, how=how, on=on)
    return df

def get_author_books(df_books, author):
    df_author = df_books.loc[df_books['Book-Author'] == author]
    return df_author

def search_rating_by_isbn(df_ratings, ISBN):
    df = df_ratings.loc[df_ratings['ISBN'] == ISBN] 
    return df

def search_author_by_isbn(df_books, ISBN):
    # Given ISBN, search df_books for the author and return the author name
    df = df_books.loc[df_books['ISBN'] == ISBN]
    return df['Book-Author'].values[0] if not df.empty else None

def search_isbn_by_title(df_books, book_title):
    # Given book title, search df_books for the ISBN and return the ISBN
    df = df_books.loc[df_books['Book-Title'] == book_title]
    return df['ISBN'].values[0] if not df.empty else None

def analyse_df(df, name):
    print(f"\nBasic analysis of DataFrame {name}")
    print("==================================")
    print(f"Shape of DataFrame: {df.shape}")
    print(f"Total number of elements: {df.size}")
    print("\nData types:")
    print(df.dtypes)

    print("\nCounts of Nulls in Each Column:")
    print("==================================")
    print(df.isnull().sum())  # Counts nulls in each column
    print("\nPercentage of Nulls in Each Column:")
    null_percent = df.isnull().mean() * 100
    print(null_percent)  # Percentage of nulls in each column

    print("\nUnique Values per Column:")
    print("==================================")
    print(df.nunique())  # Number of unique values per column
    return