import os
import glob
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(os.path.dirname(__file__))
def ingest_title_csv():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'output', 'Cleaned-Books.csv')
    df = pd.read_csv(data_path)
    return df



def preprocess_text(text):
    #Convert to lowercase
    text = text.lower()
    # Remove punctuation marks
    text = re.sub(r'[^\w\s]', '', text)
    # Separate words
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Stem extraction
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    # Combine processed words into a string
    return ' '.join(words)


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df = ingest_title_csv()
    df['Preprocessed-Title'] = df['Book-Title'].apply(preprocess_text)
    df.to_csv(os.path.join(base_dir, 'output', 'Cleaned-Books.csv'), index=False)

if __name__ == "__main__":
    main()