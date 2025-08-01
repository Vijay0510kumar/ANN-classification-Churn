import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle
from tensorflow.keras.models import load_model

# loading the trained model
model = load_model('model.h5')

# Load the encoders and scaler
with open('OneHotEncoder_geo.pkl', 'rb') as file:
    OneHotEncoder_geo = pickle.load(file)

with open('Label_encoder_gender.pkl', 'rb') as file:
    Label_encoder_gender = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file) 

# streamlit app
st.title('Customer Churn prediction')
geography = st.selectbox('Geography', OneHotEncoder_geo.categories_[0])
gender = st.selectbox('Gender', Label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# preparing the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [Label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# one hot encode geography
geo_encoded = OneHotEncoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(
    geo_encoded,
    columns=OneHotEncoder_geo.get_feature_names_out(['Geography'])
)

# combine one hot with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# scale it
input_data_scaled = scaler.transform(input_data)

# prediction
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write(f'Churn Probability : {prediction_proba:.2f}')

if prediction_proba > 0.5:
    st.write("The customer is likely to churn.")
else:
    st.write("The customer is not likely to churn.")
