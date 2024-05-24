import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import pickle

# Function to load and preprocess data
def load_and_preprocess_data(file_path):
    # Load data from a tab-separated file
    df = pd.read_csv(file_path, delimiter='\t')

    # Remove special characters and convert to lower case
    df['Product Name'] = df['Product Name'].str.replace('[^a-zA-Z\s]', '', regex=True).str.lower()
    return df

# Function for data exploration
def explore_data(df):
    # Basic information
    print("Basic Information:")
    print(df.info())
    print("\n")

    # Summary statistics
    print("Summary Statistics:")
    print(df.describe(include='all'))
    print("\n")

    # Check for missing values
    print("Missing Values (count):")
    print(df.isnull().sum())
    print("\n")

    # Display rows with null values
    print("Rows with Null Values:")
    print(df[df.isnull().any(axis=1)])
    print("\n")

    # Unique values
    print("Unique Values:")
    print(df.nunique())
    print("\n")

    # Distribution of Brands
    plt.figure(figsize=(10, 6))
    sns.countplot(y='Brand Name', data=df, order=df['Brand Name'].value_counts().index)
    plt.title('Distribution of Brand Names')
    plt.xlabel('Count')
    plt.ylabel('Brand Name')
    plt.show()

# Function to handle imbalanced data by oversampling
def handle_imbalance(df):
    # Find the maximum number of samples in any class
    max_count = df['Brand Name'].value_counts().max()
    df_balanced = pd.DataFrame()

    # Oversample each class to have the same number of samples
    for brand in df['Brand Name'].unique():
        df_brand = df[df['Brand Name'] == brand]
        df_upsampled = resample(df_brand, replace=True, n_samples=max_count, random_state=42)
        df_balanced = pd.concat([df_balanced, df_upsampled])
    
    return df_balanced

# Function to train the model
def train_model(df):
    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    X = tfidf.fit_transform(df['Product Name']).toarray()
    y = df['Brand Name']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train the model
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    # Evaluate the model using cross-validation
    skf = StratifiedKFold(n_splits=3)
    cv_scores = cross_val_score(model, X_train, y_train, cv=skf)
    print(f'Cross-Validation Accuracy Scores: {cv_scores}')
    print(f'Average Cross-Validation Accuracy: {cv_scores.mean()}')

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    
    return model, tfidf, accuracy, classification_rep

# Function to save the model and vectorizer
def save_model(model, tfidf, model_path, tfidf_path):
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    with open(tfidf_path, 'wb') as tfidf_file:
        pickle.dump(tfidf, tfidf_file)

if __name__ == "__main__":
    # Path to your text file
    file_path = 'D:/Tops/VistaGrande/brand_identifier/walmart_candies.txt'

    # Load and preprocess data
    df = load_and_preprocess_data(file_path)

    # Explore the data
    explore_data(df)

    # Handle class imbalance
    df_balanced = handle_imbalance(df)

    # Train the model
    model, tfidf, accuracy, classification_rep = train_model(df_balanced)

    # Print the accuracy and classification report
    print(f'Accuracy: {accuracy}')
    print(classification_rep)

    # Save the model and vectorizer
    model_path = 'brand_identifier_model.pkl'
    tfidf_path = 'tfidf_vectorizer.pkl'
    save_model(model, tfidf, model_path, tfidf_path)
    print(f'Model and vectorizer saved to {model_path} and {tfidf_path}')
