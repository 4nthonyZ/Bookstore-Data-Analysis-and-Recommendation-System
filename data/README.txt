README for BX Datasets

Descriptions
---------------
This repository contains three main datasets and three optional sets related to books from the BX community. These datasets include information about books, ratings given by users, and user details.

# MAIN DATASETS #

BX-Books.csv
- **ISBN**: International Standard Book Number, a unique identifier for books.
- **Book-Title**: Title of the book.
- **Book-Author**: Author(s) of the book.
- **Year-Of-Publication**: Year when the book was published.
- **Book-Publisher**: Publisher of the book.
- Total Rows: 18,185

BX-Ratings.csv
- **User-ID**: Unique identifier for users.
- **ISBN**: International Standard Book Number, a unique identifier for books.
- **Book-Rating**: Rating given by users to books.
- Total Rows: 204,146

BX-Users.csv
- **User-ID**: Unique identifier for users.
- **User-City**: City where the user is located.
- **User-State**: State where the user is located.
- **User-Country**: Country where the user is located.
- **User-Age**: Age of the user.
- Total Rows: 48,299

# DATA SETS FOR RECOMMENDATION SYSTEMS #

BX-NewBooks.csv
- **ISBN**: International Standard Book Number, a unique identifier for books.
- **Book-Title**: Title of the book.
- **Book-Author**: Author(s) of the book.
- **Year-Of-Publication**: Year when the book was published.
- **Book-Publisher**: Publisher of the book.
- Total Rows: 8,924

BX-NewBooks-Ratings.csv
- **User-ID**: Unique identifier for users.
- **ISBN**: International Standard Book Number, a unique identifier for books.
- **Book-Rating**: Rating given by users to books.
- Total Rows: 26,772

BX-NewBooks-Users.csv
- **User-ID**: Unique identifier for users.
- **User-City**: City where the user is located.
- **User-State**: State where the user is located.
- **User-Country**: Country where the user is located.
- **User-Age**: Age of the user.
- Total Rows: 8,520


Merging Datasets Using Foreign Keys
---------------------------------------------------
To merge these datasets, you can use the common field `ISBN` in BX-Books.csv and BX-Ratings.csv. Similarly, `User-ID` can be used as a foreign key to merge BX-Ratings.csv and BX-Users.csv.

Here's a sample Python code to merge the datasets using pandas:

```python
# Merge ratings with books
merged_data = pd.merge(ratings, books, on='ISBN', how='inner')

# Merge merged_data with users
merged_data = pd.merge(merged_data, users, on='User-ID', how='inner')

```

Subsampling from Large Datasets
----------------------------------------------
Working with large datasets can be computationally intensive. If you encounter performance issues, you can subsample the datasets to work with smaller portions. Here's a way to sensibly subsample the datasets:

```python
# Subsample from books
subsample_books = books.sample(n=1000, random_state=42)

# Get sampled ISBNs
sampled_isbns = subsample_books['ISBN']

# Subsample from ratings based on sampled ISBNs
subsample_ratings = ratings[ratings['ISBN'].isin(sampled_isbns)]

# Get sampled User-IDs from subsample_ratings
sampled_user_ids = subsample_ratings['User-ID']

# Subsample from users based on sampled User-IDs
subsample_users = users[users['User-ID'].isin(sampled_user_ids)]
```

Users can adjust the sample sizes according to their computational resources and analysis requirements.

