import re
import pickle

# Function to load the model and vectorizer
def load_model(model_path, tfidf_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(tfidf_path, 'rb') as tfidf_file:
        tfidf = pickle.load(tfidf_file)
    return model, tfidf

# Function to predict the brand name from a product description
def predict_brand(model, tfidf, product_description):
    # Preprocess the input
    product_description = product_description.lower()
    product_description = re.sub('[^a-zA-Z\s]', '', product_description)

    # Transform the input using the trained TF-IDF vectorizer
    X_input = tfidf.transform([product_description]).toarray()

    # Predict the brand name
    brand_name = model.predict(X_input)[0]
    return brand_name
