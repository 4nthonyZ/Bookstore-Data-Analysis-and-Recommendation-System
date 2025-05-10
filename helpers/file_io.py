import os
import glob
import pandas as pd
import re

def custom_title_case(value):
    # Regular expression to find words in a string
    def repl_func(m):
        """ Process each regex match """
        word = m.group(0)
        # Capitalize the first letter and lower the rest, special handling for apostrophes
        if "'" in word:
            parts = word.split("'")
            return parts[0].capitalize() + "'" + parts[1].lower()
        else:
            return word.capitalize()
    
    return re.sub(r"[A-Za-z]+'[A-Za-z]+|[A-Za-z]+", repl_func, value)

def clean_value(value, capitalize=True):
    # Check if the value is NaN, if so, return None
    if pd.isna(value):
        return None
    
    if isinstance(value, str):
        # Strip leading/trailing whitespace
        cleaned_value = value.strip()
        
        # Optionally capitalize each word with custom handling for apostrophes
        if capitalize:
            cleaned_value = custom_title_case(cleaned_value)
        
        # Check if the cleaned string is empty or just a dash
        if cleaned_value in ('', '-', 'N/A'):
            return None
        
        return cleaned_value
    
    return value


## Delete Files
def clear_output_dir():
    files = glob.glob('output/*')
    for f in files:
        os.remove(f)
    return

## CSV data ingestion
def get_base_dir():
    return os.path.dirname(os.path.realpath(__file__))

def ingest_csv(path_to_csv):
    # Ingests csv file from specified file path and returns as a pandas DataFrame
    df = pd.read_csv(path_to_csv)
    return df

## Ingest from data/ directory
def ingest_books_csv():
    # Ingests csv file from data directory and returns as a pandas DataFrame
    data_path = os.path.join(get_base_dir(), '..', 'data', 'BX-Books.csv')
    df = ingest_csv(data_path)
    df['Book-Title'] = df['Book-Title'].map(clean_value)
    df['Book-Author'] = df['Book-Author'].map(clean_value)
    return df

def ingest_ratings_csv():
    # Ingests csv file from data directory and returns as a pandas DataFrame
    data_path = os.path.join(get_base_dir(), '..', 'data', 'BX-Ratings.csv')
    df = ingest_csv(data_path)
    return df

def ingest_users_csv():
    # Ingests csv file from data directory and returns as a pandas DataFrame
    data_path = os.path.join(get_base_dir(), '..', 'data', 'BX-Users.csv')
    df = ingest_csv(data_path)
    # Preprocess data
    ## Remove four " from the User-City and User-Age column
    df['User-Country'] = df['User-Country'].str.replace('"', '', regex=False)
    df['User-Age'] = df['User-Age'].str.replace('"', '', regex=False)
    df = df.map(clean_value)
    return df

def ingest_all():
    # Ingests all csv files from data directory and returns df_books, df_ratings, df_users
    return ingest_books_csv(), ingest_ratings_csv(), ingest_users_csv()

## Ingest from output/ directory

def ingest_userratingscount_csv():
    # Ingests UserRatingsCount.csv file from output directory and returns as a pandas DataFrame
    data_path = os.path.join(get_base_dir(), '..', 'output', 'UserRatingsCount.csv')
    df = ingest_csv(data_path)
    return df

def ingest_user_info():
    data_path = os.path.join(get_base_dir(), '..', 'output', 'UserInfo.csv')
    df = ingest_csv(data_path)
    return df

def ingest_author_info():
    data_path = os.path.join(get_base_dir(), '..', 'output', 'AuthorInfo.csv')
    df = ingest_csv(data_path)
    return df   

def ingest_book_info():
    data_path = os.path.join(get_base_dir(), '..', 'output', 'BookInfo.csv')
    df = ingest_csv(data_path)
    return df

def ingest_city_info():
    data_path = os.path.join(get_base_dir(), '..', 'output', 'LocationInfo.csv')
    df = ingest_csv(data_path)
    return df
def ingest_CB_csv():
    data_path = os.path.join(get_base_dir(), '..', 'output', 'Cleaned-Books.csv')
    df = ingest_csv(data_path)
    return df
## Create csv
def create_csv(df, path_to_csv):
    try:
        df.to_csv(path_to_csv, encoding='utf-8', index=False)
    except:
        Exception
    return



def create_user_ratings_count(df):
    # Creates UserRatingsCount by getting value counts of UserRatings csv
    df_user_ratings_count = df['User-ID'].value_counts().rename_axis('unique_values').reset_index(name='counts')
    create_csv(df_user_ratings_count, "output/UserRatingsCount.csv")
    return df_user_ratings_count

##Test function and generate new data to detect the effect of cleaning
def main():
    df_users = ingest_users_csv()
    df_books = ingest_books_csv()
    new_csv_path = os.path.join(get_base_dir(), '..', 'output', 'CleanedUsers.csv')
    create_csv(df_users, new_csv_path)
    new_csv_path = os.path.join(get_base_dir(), '..', 'output', 'CleanedBooks.csv')
    create_csv(df_books, new_csv_path)
    
    print(f"Cleaned data saved to {new_csv_path}")

if __name__ == "__main__":
    main()
