import pandas as pd
from helpers.file_io import ingest_all,ingest_CB_csv,clear_output_dir, create_csv

import author_information
import user_information
import book_information
import loop
import item_item_preprocessing
import helpers.grouping
import helpers.title_pre
import test_item_item_similarity

def main():
    # Clean output directory
    print("Cleaning output directory...")
    clear_output_dir()
    
    # Ingest cleaned data files as dataframes
    print("Ingesting and cleaning raw Books, Ratings, and Users files")
    df_books, df_ratings, df_users = ingest_all()

    # Write cleaned dataframes to output directory
    create_csv(df_books, "output/Cleaned-Books.csv")
    create_csv(df_ratings, "output/Cleaned-Ratings.csv")
    create_csv(df_users, "output/Cleaned-Users.csv")

    # Create Authors, Users, Books, Location info in output directory
    print("Create and output author, user, book, and location information files to output directory")
    df_author_info = author_information.main(df_books, df_ratings)
    df_user_info = user_information.main(df_books, df_ratings, df_users)
    df_book_info, df_location_info = book_information.main(df_books, df_ratings, df_users)

    # Data preprocessing for machine learning 
    print("Performing data pre-processing for machine learning tasks...")
    item_item_preprocessing.main()
    helpers.title_pre.main()
    helpers.grouping.main()
    df_nb_info= ingest_CB_csv()

    # Begin interactive loop
    print("\n Welcome to our program!")
    loop.main(df_author_info, df_book_info, df_user_info,df_nb_info)

    # Test the item-item based collaborative filtering
    user_input = input("\nCalculate the Root Mean Squared Error for the Item-Item Matrix? y/n\n")
    if user_input == "y":
        print("\nCalculating Root Mean Squared Error for item-item matrix: ")
        test_item_item_similarity.main()
    else:
        print("Terminating program.")
    return

if __name__ == "__main__":
    main()