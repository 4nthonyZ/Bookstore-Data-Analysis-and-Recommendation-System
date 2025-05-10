import item_item_recommendation
from helpers.data_processing import search_isbn_by_title
from fuzzywuzzy import process
import pandas as pd
import re

def title_case(text):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(),
                  text)


def main(df_author_info, df_book_info, df_user_info, df_nb_info):
    state = "main menu"

    while(True):
        if state == "main menu":
            print("\n **** Main Menu ****\n")
            print("What would you like to do?\n"
                  "1. Recommend Books Based on a User's Favourite Book\n"
                  "2. Author Information\n"
                  "3. Book Information\n"
                  "10. Exit")
            user_input = input("\nPlease make a selection.\n")
            try:
                int(user_input)
                if user_input == "1":
                    state = "user information"
                elif user_input == "2":
                    state = "author information"
                elif user_input == "3":
                    state = "book information"
                elif user_input == "10":
                    state = "terminated"
                else:
                    print("\nPlease select a number from the menu above\n")
            except:
                print("\n****Input must be a number****\n")

        elif state == "user information":
            user_input = input("\nPlease enter the User ID\n")
            try: 
                int(user_input)
                if int(user_input) in df_user_info['User-ID'].values:
                
                    df_user = df_user_info.loc[df_user_info['User-ID'] == int(user_input)]
                    print(df_user)
                    isbn = search_isbn_by_title(df_book_info, df_user['Favourite-Books'].iloc[0])
                    print(f"Recommending books based on user {df_user['User-ID'].iloc[0]} favourite book {df_user['Favourite-Books'].iloc[0]}")
                    item_item_recommendation.main(isbn)
                else:
                    print("\nUser not found") 
            except:
                print("\n****Input must be a number****\n")     


            state = "main menu"
        
        elif state == "book information":
            print("\n1. Show Top 10 Highest Rated Books (of books with more than 30 ratings)\n"
                  "2. Show Top 10 Most Popular Books (based on number of ratings)\n"
                  "3. Search Books\n"
                  "4. Recommend Books Similar To Another Book You Like\n")
            user_input = input("Please make a selection\n")
            if user_input == "1":
                print("\nTop Ten Highest Rated Books (Minimum 30 Ratings)\n")
                print(df_book_info[df_book_info['Number of Ratings'] >= 30].sort_values(by=['Average Rating'], ascending=False).head(10))
            elif user_input == "2":
                print("\nTop Ten Most Popular Books (By Number of Ratings)\n")
                print(df_book_info.sort_values(by=['Number of Ratings'], ascending=False).head(10))
            elif user_input == "3":
                print("\nSearch by: \n"
                      "1. ISBN\n"
                      "2. Book Title\n")
                user_input = input("Please make a selection\n")
                if user_input == "1":
                    user_input = input("\nPlease enter ISBN\n")
                    if user_input in df_book_info['ISBN'].values:
                        user_input = df_book_info.loc[df_book_info['ISBN'] == user_input, 'Book-Title'].values[0]
                    else:
                        print("\nISBN not found.")
                        print("Did you mean...")
                        top_matches = process.extract(user_input, df_nb_info['ISBN'], limit=5)
                        df_matches = pd.DataFrame(top_matches, columns=['Matched ISBN', 'Score', 'DN'])
                        print(df_matches[['Matched ISBN', 'Score']])
                        state = "main menu"
                        continue
                elif user_input == "2":
                    user_input = input("\nPlease enter Book Title\n")
                
                user_input = title_case(user_input)

                if user_input in df_nb_info['Book-Title'].values:
                    print(df_book_info.loc[df_book_info['Book-Title'] == user_input])
                    cluster_id = df_nb_info.loc[df_nb_info['Book-Title'] == user_input, 'Cluster'].iloc[0]
                    cluster_books = df_nb_info[df_nb_info['Cluster'] == cluster_id]
                    unique_books = cluster_books[cluster_books['Book-Title'] != user_input].drop_duplicates(subset='Book-Title')
                    print("\nHere are some books with similar titles to your search:")
                    count = 0
                    for _, row in unique_books.iterrows():
                        print(f"{row['Book-Title']} by {row['Book-Author']}, Year Published: {row['Year-Of-Publication']}, Publisher: {row['Book-Publisher']}, ISBN: {row['ISBN']}")
                        count += 1
                        if count == 5:
                            break
                else:
                    print("\nBook not found.")
                    print("Did you mean...")
                    top_matches = process.extract(user_input, df_nb_info['Book-Title'], limit=5)
                    df_matches = pd.DataFrame(top_matches, columns=['Matched Book', 'Score', 'DN'])
                    print(df_matches[['Matched Book', 'Score']])
            elif user_input == "4":
                print("\nSearch by: \n"
                      "1. ISBN\n"
                      "2. Book Title\n")
                user_input = input("Please make a selection\n")
                if user_input == "1":
                    user_input = input("Please enter the ISBN: \n")
                    if user_input in df_book_info['ISBN'].values:
                        print(f"\nRecommending books based on books that users who enjoyed {df_book_info.loc[df_book_info['ISBN'] == user_input, 'Book-Title'].values[0]} also enjoyed")
                        item_item_recommendation.main(user_input)
                    else:
                        print("\nISBN not found")
                        print("Did you mean...")
                        top_matches = process.extract(user_input, df_nb_info['ISBN'], limit=5)
                        df_matches = pd.DataFrame(top_matches, columns=['Matched ISBN', 'Score', 'DN'])
                        print(df_matches[['Matched ISBN', 'Score']])
                elif user_input == "2":
                    user_input = input("\nPlease enter the Book Title: \n")
                    user_input = title_case(user_input)
                    if user_input in df_book_info['Book-Title'].values:
                        print(f"\nRecommending books based on books that users who enjoyed {user_input} also enjoyed")
                        isbn = search_isbn_by_title(df_book_info, user_input)
                        item_item_recommendation.main(isbn)
                    else:
                        print("\nBook not found")
                        print("Did you mean...")
                        top_matches = process.extract(user_input, df_nb_info['Book-Title'], limit=5)
                        df_matches = pd.DataFrame(top_matches, columns=['Matched Book', 'Score', 'DN'])
                        print(df_matches[['Matched Book', 'Score']])
            state = "main menu"


        elif state == "author information":
            print("\n1. Top 10 Highest Rated Authors (of authors with more than 30 ratings)\n"
                  "2. Top 10 Most Popular Authors (by number of ratings)\n"
                  "3. Search Author")
            user_input = input("\nPlease make a selection\n")
            if user_input == "1":
                print("\nTop 10 Highest Rated Authors (Minimum 30 Ratings)\n")
                print(df_author_info[df_author_info['TotalRatings'] >= 30].sort_values(by=['AverageRating'], ascending=False).head(10))
            elif user_input == "2":
                print("\nTop Ten Most Popular Authors (By Number of Ratings)\n")
                print(df_author_info.sort_values(by=['TotalRatings'], ascending=False).head(10))
            elif user_input == "3":
                user_input = input("Please enter Author Full Name\n")
                user_input = title_case(user_input)
                if user_input in df_author_info['Book-Author'].values:
                    print("\nAuthor Information")
                    print(df_author_info.loc[df_author_info['Book-Author'] == user_input])
                    print("\nList of Author's Books")
                    print(df_book_info.loc[df_book_info['Book-Author']==user_input])
                else:
                    print("\nAuthor not found")
                    print("Did you mean...")
                    top_matches = process.extract(user_input, df_nb_info['Book-Author'], limit=5)
                    df_matches = pd.DataFrame(top_matches, columns=['Matched Author', 'Score', 'DN'])
                    print(df_matches[['Matched Author', 'Score']].drop_duplicates())
            state = "main menu"

    
        if state == "terminated":
            print("Thank you for using our program!")
            break
    return

if __name__ == "__main__":
    main()