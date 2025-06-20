import joblib
import pandas as pd
import streamlit as st

sample_data = pd.read_csv('data/student.csv', delimiter=';').sample(1)

scaler = joblib.load('model/scaler.joblib')
model = joblib.load('model/model.joblib')
features = joblib.load('model/features.joblib')

all_features = ['Marital_status', 'Application_mode', 'Application_order', 'Course',
                'Daytime_evening_attendance', 'Previous_qualification',
                'Previous_qualification_grade', 'Nacionality', 'Mothers_qualification',
                'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation',
                'Admission_grade', 'Displaced', 'Educational_special_needs', 'Debtor',
                'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder',
                'Age_at_enrollment', 'International',
                'Curricular_units_1st_sem_credited',
                'Curricular_units_1st_sem_enrolled',
                'Curricular_units_1st_sem_evaluations',
                'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade',
                'Curricular_units_1st_sem_without_evaluations',
                'Curricular_units_2nd_sem_credited',
                'Curricular_units_2nd_sem_enrolled',
                'Curricular_units_2nd_sem_evaluations',
                'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
                'Curricular_units_2nd_sem_without_evaluations', 'Unemployment_rate',
                'Inflation_rate', 'GDP']

for feature_name in all_features:
    print()


def preprocessing_input(input_data):
    scaled = scaler.transform(input_data)
    processed_data = pd.DataFrame(scaled, columns=input_data.columns)

    return processed_data[features['Features'].tolist()]


def predict(input_data):
    processed_data = preprocessing_input(input_data)
    prediction = model.predict(processed_data)

    result = None

    if prediction == 0:
        result = 'Dropout'
    elif prediction == 1:
        result = 'Enrolled'
    elif prediction == 2:
        result = 'Graduate'

    return result


# STREAMLIT
col1, col2 = st.columns([1, 5])
with col1:
    st.image(
        "https://png.pngtree.com/png-clipart/20230928/original/pngtree-education-school-logo-design-college-academic-student-vector-png-image_12898007.png",
        width=200)
with col2:
    st.title("Sistem Prediksi Status Mahasiswa")

input_student = {}

st.header("Masukkan Data Mahasiswa:")

col1, col2 = st.columns([1, 1])

for i, feature_name in enumerate(all_features):
    label = feature_name.replace('_', ' ').title()

    if i % 2 == 0:
        with col1:
            input_student[feature_name] = st.number_input(label, key=feature_name, value=0)
    else:
        with col2:
            input_student[feature_name] = st.number_input(label, key=feature_name, value=0)

st.header('Student Detail')
cols = st.columns(5)

items = list(input_student.items())

for i, (key, value) in enumerate(items):
    formatted_label = key.replace('_', ' ').title()

    with cols[i % len(cols)]:
        st.metric(label=formatted_label, value=value)

st.header('Prediction')

df_input_student = pd.DataFrame(input_student, columns=all_features, index=[0])

if st.button("🚀 Prediksi Status Mahasiswa", type="primary", use_container_width=True):

    final_result = predict(df_input_student)

    st.subheader("Hasil Prediksi:")

    if final_result == 'Graduate':
        st.success(f"🎉 Selamat! Mahasiswa diprediksi akan **LULUS** (Graduate).", icon="🎓")
    elif final_result == 'Enrolled':
        st.info(f"💡 Mahasiswa diprediksi masih **TERDAFTAR** (Enrolled).", icon="🧑‍💻")
    elif final_result == 'Dropout':
        st.error(f"⚠️ Perhatian! Mahasiswa diprediksi berisiko **DO** (Dropout).", icon="🔥")
