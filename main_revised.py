import streamlit as st
import pandas as pd
import pickle as pkl
from PIL import Image

primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

# Header
st.write("""# Endoscopic intervention prediction""")

# Sidebar
st.sidebar.header('User Input Parameters')

def user_input_features():

    layout = st.sidebar.columns([1, 1])

    with layout[0]:
        Sex = st.radio("Gender",('Male', 'Female'), horizontal=True)
        Cirrhosis = st.radio("Cirrhosis", ('No', 'Yes'), horizontal=True)
        Drugs = st.radio("Antithrombotic drugs", ('No', 'Yes'), horizontal=True)
        Hematemesis = st.radio("Red emesis", ('No', 'Yes'), horizontal=True)
        Coffeeground = st.radio("Coffee ground", ('No', 'Yes'), horizontal=True)
        Melena = st.radio("Melena", ('No', 'Yes'), horizontal=True)
        Maroon = st.radio("Maroon stool", ('No', 'Yes'), horizontal=True)
        Hematochezia = st.radio("Red stool", ('No', 'Yes'), horizontal=True)
        SBP = st.text_input('Systolic BP (mmHg)', '120')
        Hb = st.text_input('Hemoglobin level (g/dL)', '10')
        INR = st.text_input('INR', '1.0')
        BUN = st.text_input('BUN (mg/dL)', '20')

    with layout[-1]:
        Age = st.text_input('Age (yr)', '60')
        Malignancy = st.radio("Malignancy", ('Yes', 'No'), horizontal=True)
        PrevUGIB = st.radio("Hx UGIB", ('No', 'Yes'), horizontal=True)
        Onset = st.text_input('Time to presentation(hr)', '0')
        HR = st.text_input('Heart rate (bpm)', '80')
        Plt = st.text_input('Platelet count (x10^6/ml)', '200')
        Alb = st.text_input('Albumin level (g/dL)', '4.0')
        Cr = st.text_input('Creatinine (mg/dL)', '1.0')

    Resus = st.sidebar.radio("Resuscitation", ('None', 'IV loading','Vasopressor'), horizontal=True)

    data = {'Sex': Sex,
            'Cirrhosis': Cirrhosis,
            'Drugs': Drugs}

    features = pd.DataFrame(data, index=[0])

    return features


df = user_input_features()

st.write(df)


# st.write(df)
#
# # loading in the model to predict on the data
# # pickle_in1 = open('abstract model.pkl', 'rb')
# # classifier1 = pkl.load(pickle_in1)
#
# # prediction1 = classifier1.predict(
#         # [[Sex, Cirrhosis, petal_length1, petal_width1]])
#    # print(prediction1)
#
# st.header('Result:')
# st.subheader('Need intervention')
#
# st.header('Prediction probability:')
# st.subheader("86%")

