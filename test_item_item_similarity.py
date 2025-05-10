import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import pickle
import numpy as np
from math import sqrt

import os
import matplotlib.pyplot as plt

def load_data():
    books = pd.read_csv('output/Cleaned-Books.csv', usecols=['ISBN', 'Book-Title', 'Book-Author'], dtype={'ISBN': str})
    ratings = pd.read_csv('output/Cleaned-Ratings.csv', dtype={'User-ID': int, 'ISBN': str, 'Book-Rating': int})
    return books, ratings

def create_sparse_user_item_matrix(ratings):
    matrix = ratings.pivot(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
    sparse_matrix = csr_matrix(matrix.values)
    return sparse_matrix, matrix.index, matrix.columns

def calculate_sparse_similarity(sparse_matrix):
    return cosine_similarity(sparse_matrix.transpose(), dense_output=False)

def save_objects(obj, filename, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, filename), 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def predict_ratings(user_id, item_ids, item_similarity, all_ratings):
    user_ratings = all_ratings[all_ratings['User-ID'] == user_id]
    predictions = []
    valid_indices = []  # To track indices where predictions are valid

    # Using a dictionary for fast lookup of item index
    item_index_map = {item: idx for idx, item in enumerate(item_ids)}

    for isbn, actual_rating in user_ratings[['ISBN', 'Book-Rating']].values:
        if isbn in item_index_map:
            sim_scores = item_similarity.getrow(item_index_map[isbn]).toarray().flatten()
            indices = [item_index_map[rated_isbn] for rated_isbn in user_ratings['ISBN'] if rated_isbn in item_index_map]
            valid_sim_scores = sim_scores[indices]
            valid_ratings = [r for i, r in user_ratings[['ISBN', 'Book-Rating']].values if i in item_index_map]

            if np.sum(valid_sim_scores) > 0 and len(valid_sim_scores) == len(valid_ratings):
                predicted_rating = np.dot(valid_sim_scores, valid_ratings) / np.sum(valid_sim_scores)
                predictions.append(predicted_rating)
                valid_indices.append(item_index_map[isbn])  # Store the index of the valid prediction
            else:
                continue  # Skip appending if no valid prediction can be made
        else:
            continue  # Skip if the ISBN is not in the map

    return predictions, valid_indices


def main():
    books, ratings = load_data()
    train_ratings, test_ratings = train_test_split(ratings, test_size=0.1, random_state=99)
    train_sparse_matrix, user_index, item_ids = create_sparse_user_item_matrix(train_ratings)
    item_similarity = calculate_sparse_similarity(train_sparse_matrix)

    test_user_ids = test_ratings['User-ID'].unique()

    actual, preds = [], []
    for user_id in test_user_ids:
        user_actual_ratings = test_ratings[test_ratings['User-ID'] == user_id]
        if not user_actual_ratings.empty:
            user_pred_ratings, valid_indices = predict_ratings(user_id, list(item_ids), item_similarity, test_ratings)
            # Match actual ratings with valid predictions
            actual.extend(user_actual_ratings.loc[user_actual_ratings['ISBN'].isin([item_ids[i] for i in valid_indices]), 'Book-Rating'].tolist())
            preds.extend(user_pred_ratings)

    if preds:
        rmse = sqrt(mean_squared_error(actual, preds))
        print("Root Mean Squared Error: ", rmse)
    else:
        print("No valid predictions or actual ratings were collected.")

    # Scatter Plot of Predictions vs. Actuals
    plt.figure(figsize=(10, 5))
    plt.scatter(actual, preds, alpha=0.1)
    plt.xticks(range(1, 11))
    plt.yticks(range(1, 11))
    plt.xlabel('Actual Ratings')
    plt.ylabel('Predicted Ratings')
    plt.title('Actual vs. Predicted Ratings')
    plt.plot([1, 10], [1, 10], 'r--')  # Line showing perfect predictions
    plt.grid(True)
    plt.savefig("output/item_item_testing_scatterplot.png")
    plt.show()
    return

if __name__ == "__main__":
    main()
