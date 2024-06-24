import streamlit as st
import pandas as pd
import datetime as dt
from PIL import Image
from pycaret.classification import load_model
from pathlib import Path

st.set_page_config(
    page_title="Endoscopic intervention prediction",
    layout="wide",
    initial_sidebar_state="expanded",)

st.markdown("<style>.stTextInput  > label {font-size:50%; color:black; border: 2px ;border-radius: 3px;}"
            "</style>",unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.write(' ')

with col3:
    image = Image.open('Logo.png')
    st.image(image)

# Header
st.header("Endoscopic intervention prediction")

# Content
image = Image.open('egd1.jpg')
st.image(image)

# Sidebar
st.sidebar.header('Input Parameters')

hosp = st.sidebar.selectbox('Hospital',('Siriraj','Golden Jubilee','Rama','Nakornsawan'))

def user_input_features():

    layout = st.sidebar.columns([1, 1])

    with layout[0]:
        Age = st.number_input('Age (yr)', 0)
        Sex_gr = st.radio("Gender",('Male', 'Female'), horizontal=True)
        Cirrhosis_gr2 = st.radio("Cirrhosis", ('No', 'Yes'), horizontal=True)
        CA_gr2 = st.radio("Malignancy", ('No', 'Yes'), horizontal=True)
        HxUGIB_gr = st.radio("Hx UGIB", ('No', 'Yes'), horizontal=True)
        Medication_gr2 = st.radio("Antithrombotic drugs", ('No', 'Yes'), horizontal=True)
        Vomit_type = st.selectbox("Vomit type", ('Red emesis','Coffee ground','Normal'))
        Stool_type = st.selectbox("Stool type", ('Hematochezia','Maroon','Melena','Normal'))
        Onset = st.number_input('Time to presentation(hr)', 0)
        Resus_gr2 = st.radio("Resuscitation", ('No', 'Yes'), horizontal=True)

    with layout[-1]:
        SBP = st.number_input('Systolic BP (mmHg)', 0)
        HR = st.number_input('Heart rate (bpm)', 0)
        Hb = st.number_input('Hemoglobin level (g/dL)', 0.0)
        Plt = st.number_input('Platelet count (x10^6/ml)', 0)
        INR = st.number_input('INR', 0.00)
        BUN = st.number_input('BUN (mg/dL)', 0.00)
        Cr = st.number_input('Creatinine (mg/dL)', 0.1)
        Alb = st.number_input('Albumin level (g/dL)', 0.0)

    data = {'Sex_gr': Sex_gr,'Age': Age, 'Cirrhosis_gr2': Cirrhosis_gr2,'CA_gr2':CA_gr2,'Medication_gr2': Medication_gr2, 'Hx UGIB_gr': HxUGIB_gr,'Onset': Onset, 'Resus_gr2': Resus_gr2,
             'Vomit type': Vomit_type,'Stool type': Stool_type,'SBP': SBP,'HR': HR, 'Hb':Hb, 'Plt':Plt*1000, 'INR': INR, 'Alb': Alb, 'BUN Cr': BUN/Cr}

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

# loading in the model to predict on the data
final_lda = load_model('abstract model')
myfile = Path('./datacollect.csv')

if st.sidebar.button('Predict'):
#    st.write('click')
    if df.eq(0).any().any():
        st.write('Please fill all the data')
    else:
#       st.write('Ready for prediction')
        predict_value = final_lda.predict(df)
        prob = final_lda.predict_proba(df)
        if predict_value == 0:
            rimage = Image.open('GIBleed.jfif')
            st.subheader('Result: No need for endoscopic intervention with probability '+ str("{:.2f}".format(prob[0][0]*100)) +'%')
        elif predict_value == 1:
            rimage = Image.open('Logo.png')
            st.subheader('Result: Need for endoscopic intervention with probability ' + str("{:.2f}".format(prob[0][1]*100)) +'%')
        else:
            print('ERROR')

    df['predicted value'] = predict_value
    df['prob for negative class'] = prob[0][0]
    df['prob for positive class'] = prob[0][1]

    outdf = pd.DataFrame([{'UTC Timestamp': dt.datetime.now(), 'Hospital': hosp}])
    outdf = pd.concat([outdf, df], axis=1)

    if myfile.is_file():
        st.write('file existed')
        outdf.to_csv('datacollect.csv', mode='a', index=False, header=False)
    else:
        outdf.to_csv('datacollect.csv', index=False)

#  #   st.image(rimage.resize((200, 200)))

if myfile.is_file():
    collecteddf = pd.read_csv('datacollect.csv')

    st.download_button(
        label="Download CSV",
        data=collecteddf.to_csv().encode("utf-8"),
        file_name="collecteddata.csv",
        mime="text/csv"
    )