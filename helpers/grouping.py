import numpy as np
import os
import glob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
base_dir = os.path.dirname(os.path.dirname(__file__))


def adjust_clusters(df, labels, centers, tfidf_matrix, min_size=5, max_size=40):
    cluster_sizes = np.bincount(labels, minlength=len(centers))
    small_clusters = np.where(cluster_sizes < min_size)[0]
    large_clusters = np.where(cluster_sizes > max_size)[0]
    center_distances = euclidean_distances(centers)
    np.fill_diagonal(center_distances, np.inf)

    # Handle small clusters
    for cluster_id in small_clusters:
        if cluster_sizes[cluster_id] < min_size:
            nearest_cluster = np.argmin(center_distances[cluster_id])
            df.loc[df['Cluster'] == cluster_id, 'Cluster'] = nearest_cluster
            cluster_sizes[nearest_cluster] += cluster_sizes[cluster_id]
            cluster_sizes[cluster_id] = 0

    # Handle large clusters
    for cluster_id in large_clusters:
        if cluster_sizes[cluster_id] > max_size:
            cluster_indices = df[df['Cluster'] == cluster_id].index
            num_subclusters = (cluster_sizes[cluster_id] // max_size) + (cluster_sizes[cluster_id] % max_size != 0)
            sub_kmeans = KMeans(n_clusters=num_subclusters, random_state=0)
            sub_labels = sub_kmeans.fit_predict(tfidf_matrix[cluster_indices])
            df.loc[cluster_indices, 'Cluster'] = sub_labels + df['Cluster'].max() + 1  # Ensure unique tags

    return df



def ingest_title_csv():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'output', 'Cleaned-Books.csv')
    df = pd.read_csv(data_path)
    return df




def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df = ingest_title_csv()

    # Extract TF-IDF features from the book titles
    vectorizer = TfidfVectorizer(max_features=18186)
    df.columns = df.columns.str.strip()
    df['Preprocessed-Title'] = df['Preprocessed-Title'].astype(str)
    tfidf_matrix = vectorizer.fit_transform(df['Preprocessed-Title'])

    # Apply K-means clustering
    num_clusters = 900
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(tfidf_matrix)
    labels = kmeans.labels_

    # Adjust clusters to ensure each has at least 10 books
    df['Cluster'] = labels  # Add cluster labels to the original DataFrame
    adjusted_df = adjust_clusters(df, labels, kmeans.cluster_centers_, tfidf_matrix)
    df['Cluster'] = adjusted_df['Cluster']  # Update df with adjusted clusters

    # Save the DataFrame with cluster labels
    df.to_csv(os.path.join(base_dir, 'output', 'Cleaned-Books.csv'), index=False)

if __name__ == "__main__":
    main()