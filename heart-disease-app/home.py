import streamlit as st

import utils
import utils as util
#===================== App Config ===========================#

st.set_page_config(
    layout='centered',
    page_title='Health App'
)

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_page(page: str, **kwargs):
    st.session_state.page = page
    for key, value in kwargs.items():
        st.session_state[key] = value
    st.rerun()

def back_to_home():
    st.session_state.page = 'home'
    st.rerun()

#===================== App Config Ends ===========================#

#===================== Home Page Config Starts ===========================#
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center; color='white'>Heart Disease Risk Predictor</h1>", unsafe_allow_html=True)
    st.image('images/heart-bg.png')

    col1, col2 = st.columns(2)
    with col1:
        manual_btn = st.button('Enter Data Manually',use_container_width=True)
        if manual_btn:
            go_to_page('predictor')
    with col2:
        pdf_btn = st.button('Upload Report Pdf',use_container_width=True,disabled= st.session_state.get("disabled",True))


#===================== Home Page Config Ends ===========================#

#===================== Predictor Page Config Starts ===========================#

elif st.session_state.page == 'predictor':
    patient ={}
    st.markdown("<h1 style='text-align: center; color='white'>Heart Disease Risk Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color='white'>Heart Disease Risk Assessment – Patient Data Form</h2>",unsafe_allow_html=True)

    # Patient Data Entry Form
    name = st.text_input('Enter Patient Name')
    with st.form('patient-data'):
        thalach = st.number_input('Enter Value for Thalach ',key='thalach')
        chol = st.number_input('Enter Value for Cholestrol',key='chol')
        trestbps = st.number_input('Enter Value for Trestbps',key='trestbps')
        oldpeak = st.number_input('Enter Value for Oldpeak',key='oldpeak')
        age = st.number_input('Enter Value for Age',key='Age')
        cp = st.number_input('Enter Value for CP',key='CP')
        ca = st.number_input('Enter Value for CA',key='CA')
        thal = st.number_input('Enter Value for THAL',key='thal')
        analyze_btn = st.form_submit_button('Analyze',use_container_width=True)



    if analyze_btn:
        patient['thalach'] = thalach
        patient['cp'] = cp
        patient['chol'] = chol
        patient['oldpeak'] = oldpeak
        patient['trestbps'] = trestbps
        patient['age'] = age
        patient['thal'] = thal
        patient['ca'] = ca
        input_df = utils.create_input_df(patient)
        analysis = utils.predict_patient(name, input_df)
        go_to_page('analysis',input_df=input_df,analysis = analysis)
        st.rerun()



    pred_back_btn = st.button('Back', use_container_width=True)
    if pred_back_btn:
        back_to_home()

#===================== Predictor Page Config Ends ===========================#

#===================== Analysis Page Config Starts ==========================#
elif st.session_state.page == 'analysis':
    analysis = st.session_state.get('analysis')
    patient_name = analysis['name']
    risk = analysis['risk']
    input_df = st.session_state.get('input_df')

    risk_colors = {
        "Low": "green",
        "Moderate": "yellow",
        "High": "red"
    }

    color = risk_colors.get(risk)

    st.markdown("<h1 style='text-align: center; color='white'>Heart Disease Risk Assessment</h1>",
                unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color='white'>Prediction Result for Patient: {patient_name}</h2>",
                unsafe_allow_html=True)

    st.markdown(f"""
    ### Based on the data you provided, your estimated heart disease risk category is <span style='color:{color}; font-weight:bold;'>{risk}</span>.
    """,
    unsafe_allow_html=True)

    analyzed_prediction = utils.analyze_prediction(input_df)
    st.markdown("### Top contributing factors to your risk prediction:")

    for feature, explanation in analyzed_prediction.items():
        st.markdown(f"- **{feature.capitalize()}**: {explanation}")

    col1, col2 = st.columns(2)
    with col1:
        pred_back_btn = st.button('Back', use_container_width=True)
        if pred_back_btn:
            go_to_page('predictor')

    with col2:
        home_btn = st.button('Home', use_container_width=True)
        if home_btn:
            back_to_home()
#===================== Analysis Page Config Ends ==========================#
