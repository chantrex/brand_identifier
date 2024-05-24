from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from brand_identifier import load_model, predict_brand

# These libraries are used with Pytesseract:
# import pytesseract
# import io

app = FastAPI()

# Paths to the saved model and vectorizer
MODEL_PATH = 'brand_identifier_model.pkl'
TFIDF_PATH = 'tfidf_vectorizer.pkl'

# Allow all origins (not recommended in production mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

success_messages = [
    "Congrats! You hit the backend!",
    "Well done! Your request was successful!",
    "Success! Your operation completed perfectly!",
    "Awesome! Everything went smoothly!",
    "Great job! The backend responded as expected!"
]

@app.post('/process-text')
async def process_text(request: Request):
    data = await request.json()
    product_description = data.get('text', '')

    # Load the model and vectorizer
    model, tfidf = load_model(MODEL_PATH, TFIDF_PATH)

    # Example product description
    # product_description = "Dove Promises, Sea Salt And Caramel Dark Chocolate Candy, 7.61 Oz."

    # Predict the brand name
    predicted_brand = predict_brand(model, tfidf, product_description)

    content = {
        'text_request': product_description,
        'text_result': predicted_brand
    }
    
    print(f'Predicted Brand: {predicted_brand}')
    return JSONResponse(content=content)