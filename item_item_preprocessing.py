import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def load_data():
    books = pd.read_csv('output/Cleaned-Books.csv', usecols=['ISBN', 'Book-Title', 'Book-Author'], dtype={'ISBN': str})
    ratings = pd.read_csv('output/Cleaned-Ratings.csv', dtype={'User-ID': int, 'ISBN': str, 'Book-Rating': int})
    return books, ratings

def create_sparse_user_item_matrix(ratings):
    matrix = ratings.pivot(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
    sparse_matrix = csr_matrix(matrix.values)
    return sparse_matrix, matrix.columns

def calculate_sparse_similarity(sparse_matrix):
    return cosine_similarity(sparse_matrix.transpose(), dense_output=False)

def save_objects(obj, filename):
    # Ensure the output directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, filename), 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def main():
    books, ratings = load_data()
    sparse_user_item_matrix, item_ids = create_sparse_user_item_matrix(ratings)
    item_similarity = calculate_sparse_similarity(sparse_user_item_matrix)
    
    # Save the similarity matrix and item_ids for later use
    save_objects(item_similarity, 'item_similarity.pkl')
    save_objects(item_ids, 'item_ids.pkl')

if __name__ == "__main__":
    main()
