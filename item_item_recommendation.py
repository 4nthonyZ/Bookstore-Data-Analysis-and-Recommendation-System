import pandas as pd
import pickle
import os

def load_objects(filename):
    with open(os.path.join('output', filename), 'rb') as input:
        return pickle.load(input)

def recommend_books(base_isbn, top_n=5):
    item_similarity = load_objects('item_similarity.pkl')
    item_ids = load_objects('item_ids.pkl')
    books = pd.read_csv('output/Cleaned-Books.csv', usecols=['ISBN', 'Book-Title', 'Book-Author'], dtype={'ISBN': str})

    base_index = list(item_ids).index(base_isbn)
    similarity_scores = item_similarity.getrow(base_index).toarray().flatten()
    similar_indices = similarity_scores.argsort()[::-1][1:top_n+1]
    similar_isbns = item_ids[similar_indices]
    recommended_books = books[books['ISBN'].isin(similar_isbns)]
    return recommended_books


def main(ISBN):
    recommendations = recommend_books(ISBN)
    print("Recommended Books based on ISBN", ISBN)
    print(recommendations)

if __name__ == "__main__":
    main()
