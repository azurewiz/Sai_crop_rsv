import streamlit as st
import pandas as pd
import joblib


@st.cache_resource
def load_model_and_encoder():
    model = joblib.load("C:/Users/Sai Arvind Arun/Desktop/certifications/internship/edunet shell 2025 jan/cropper/models/fertilizer_model.pkl")
    label_encoder = joblib.load("C:/Users/Sai Arvind Arun/Desktop/certifications/internship/edunet shell 2025 jan/cropper/models/label_encoder.pkl")
    return model, label_encoder

def create_crop_mapping():
    crop_mapping = {
        "rice": "Paddy",
        "maize": "Maize",
        "chickpea": "Pulses",
        "kidneybeans": "Pulses",
        "pigeonpeas": "Pulses",
        "mothbeans": "Pulses",
        "mungbean": "Pulses",
        "lentil": "Pulses",
        "black gram": "Pulses",
        "pomegranate": "Fruit",
        "banana": "Fruit",
        "mango": "Fruit",
        "grapes": "Fruit",
        "watermelon": "Fruit",
        "muskmelon": "Fruit",
        "apple": "Fruit",
        "orange": "Fruit",
        "papaya": "Fruit",
        "coconut": "Fruit",
        "cotton": "Cotton",
        "jute": "Oil Seeds",
        "coffee": "Other"
    }
    return crop_mapping


def recommend_fertilizer(crop_name, N, P, K, temperature, humidity, ph, rainfall):
    crop_mapping = create_crop_mapping()
    mapped_crop_name = crop_mapping.get(crop_name.lower(), None)

    if not mapped_crop_name:
        return "Crop not found in the database."

    
    input_features = [[N, P, K, temperature, humidity, ph, rainfall]]

    
    model, label_encoder = load_model_and_encoder()

    
    prediction = model.predict(input_features)
    fertilizer_name = label_encoder.inverse_transform(prediction)[0]
    return fertilizer_name


def main():
    st.title("Crop to Fertilizer Recommendation App")

    
    crop_name = st.text_input("Enter crop name:", "").strip().lower()
    N = st.number_input("Nitrogen (N):", min_value=0, max_value=100, value=50)
    P = st.number_input("Phosphorous (P):", min_value=0, max_value=100, value=50)
    K = st.number_input("Potassium (K):", min_value=0, max_value=100, value=50)
    temperature = st.number_input("Temperature (°C):", min_value=0.0, max_value=50.0, value=25.0)
    humidity = st.number_input("Humidity (%):", min_value=0.0, max_value=100.0, value=50.0)
    ph = st.number_input("pH:", min_value=0.0, max_value=14.0, value=7.0)
    rainfall = st.number_input("Rainfall (mm):", min_value=0.0, max_value=300.0, value=100.0)

    if st.button("Get Fertilizer Recommendation"):
        if not crop_name:
            st.error("Please enter a valid crop name.")
        else:
            recommendation = recommend_fertilizer(crop_name, N, P, K, temperature, humidity, ph, rainfall)
            st.success(f"Recommended fertilizer for {crop_name.capitalize()}: {recommendation}")

if __name__ == "__main__":
    main()