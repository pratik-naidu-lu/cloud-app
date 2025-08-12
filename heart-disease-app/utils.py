import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import joblib

# Load Prof Model
prod_heart_model = joblib.load('heart_disease_bfm_v1.joblib')

# Clinical Thresholds
clinical_thresholds = {
    'age': 55,          # Age > 55 considered higher risk
    'chol': 240,        # Cholesterol mg/dL > 240 is high
    'trestbps': 130,    # Resting BP mmHg > 130 is high
    'thalach': 100,     # Max heart rate < 100 is lower fitness
    'oldpeak': 2.0,     # ST depression > 2 indicates higher risk
    'cp': 3,            # Chest pain type (3 and 4 are more serious)
    'ca': 1,            # Number of vessels colored by fluoroscopy > 0 risky
    'thal': 3           # Thalassemia type 3 (reversible defect) higher risk
}
explanation_map = {
    'thalach' : 'Your maximum heart rate is lower than expected, which may suggest reduced heart function or fitness.',
    'age': 'Your age is a natural factor—older age increases the risk of heart disease.',
    'chol':'Your cholesterol is higher than the healthy range, increasing heart disease risk.',
    'trestbps':'Your resting blood pressure is elevated, increasing strain on your heart and vessels.',
    'oldpeak':'Your ECG shows some ST depression during exercise, which suggests possible heart illness',
    'cp':'You have a more severe type of chest pain, which can be a warning sign of heart problems.',
    'ca':'ou have multiple vessels affected, which significantly increases heart disease risk.',
    'thal':'You have a thalassemia defect which may affect heart function and increase risk.'

}
def create_input_df(patient: dict)-> DataFrame:
    input_df = pd.DataFrame(patient,index=[0])
    return input_df

def predict_patient(patient_name: str, input_df: DataFrame)-> dict:
    prediction ={}
    risk_cat = prod_heart_model.predict(input_df)

    if risk_cat == 0:
        risk = 'Low'
    elif risk_cat ==1:
        risk = 'Moderate'
    else:
        risk = 'High'

    prediction['name']=patient_name
    prediction['risk'] = risk

    print('Logging Risk Category for patient')
    print(prediction)
    calculte_deviation(input_df)

    return prediction

def calculte_deviation(input_df: DataFrame):
    deviations = {}
    deviations['thalach'] = np.maximum(0, clinical_thresholds['thalach'] - input_df['thalach'].iloc[0])
    deviations['cp'] = np.maximum(0, input_df['cp'].iloc[0] - clinical_thresholds['cp'])
    deviations['chol'] = np.maximum(0, input_df['chol'].iloc[0] - clinical_thresholds['chol'])
    deviations['oldpeak'] = np.maximum(0, input_df['oldpeak'].iloc[0] - clinical_thresholds['oldpeak'])
    deviations['trestbps'] = np.maximum(0, input_df['trestbps'].iloc[0] - clinical_thresholds['trestbps'])
    deviations['age'] = np.maximum(0, input_df['age'].iloc[0] - clinical_thresholds['age'])
    deviations['thal'] = np.maximum(0, input_df['thal'].iloc[0] - clinical_thresholds['thal'])
    deviations['ca'] = np.maximum(0, input_df['ca'].iloc[0] - clinical_thresholds['ca'])

    dev_series = pd.Series(deviations)
    print('logging deviation series')
    print(dev_series)

    print('Normalize Deviation')
    print(normalize_deviations(dev_series))
    return dev_series

def normalize_deviations(deviation_series: Series):
    min_val = deviation_series.min()
    max_val = deviation_series.max()

    if max_val - min_val ==0:
        return pd.Series(0, index=deviation_series.index)
    else:
        norm_val = (deviation_series-min_val)/(max_val - min_val)
        return norm_val


def analyze_prediction(input_df: DataFrame):
    analyzed_prediction={}
    dev_series = calculte_deviation(input_df)
    normal_devs = normalize_deviations(dev_series)
    top4_factors = normal_devs.sort_values(ascending=False).head(4)
    top4_feature_names = top4_factors.index.tolist()

    for feature in top4_feature_names:
        analyzed_prediction[feature] = explanation_map[feature]

    return analyzed_prediction

