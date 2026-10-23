import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Reproducibility
np.random.seed(42)
random.seed(42)

# Number of records
N = 50000

cities = [
    "Ahmedabad",
    "Mumbai",
    "Delhi",
    "Pune",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Surat",
    "Vadodara",
    "Jaipur"
]

genders = ["Male", "Female"]

departments = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "General Medicine",
    "Pediatrics",
    "Dermatology",
    "Oncology",
    "Emergency"
]

admission_types = [
    "Emergency",
    "Scheduled",
    "Referral"
]

diagnoses = [
    "Hypertension",
    "Diabetes",
    "Heart Disease",
    "Migraine",
    "Fracture",
    "Asthma",
    "Pneumonia",
    "Skin Infection",
    "Cancer",
    "Viral Infection"
]

treatments = [
    "Medication",
    "Surgery",
    "Therapy",
    "Observation",
    "Chemotherapy",
    "Emergency Care",
    "Diagnostic Procedure"
]

room_types = [
    "General Ward",
    "Semi-Private",
    "Private",
    "ICU"
]

patient_ids = [
    f"P{str(i).zfill(6)}"
    for i in range(1, N + 1)
]

admission_ids = [
    f"A{str(i).zfill(6)}"
    for i in range(1, N + 1)
]

doctor_ids = [
    f"D{str(random.randint(1, 100)).zfill(3)}"
    for _ in range(N)
]


start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

date_range = (end_date - start_date).days

admission_dates = [
    start_date + timedelta(
        days=random.randint(0, date_range)
    )
    for _ in range(N)
]


length_of_stay = np.random.randint(1, 16, N)

discharge_dates = [
    admission_dates[i] +
    timedelta(days=int(length_of_stay[i]))
    for i in range(N)
]

ages = np.random.randint(1, 90, N)

gender_data = np.random.choice(
    genders,
    size=N,
    p=[0.52, 0.48]
)

city_data = np.random.choice(
    cities,
    size=N
)

department_data = np.random.choice(
    departments,
    size=N
)

admission_type_data = np.random.choice(
    admission_types,
    size=N,
    p=[0.35, 0.45, 0.20]
)

diagnosis_data = np.random.choice(
    diagnoses,
    size=N
)

treatment_data = np.random.choice(
    treatments,
    size=N
)

room_data = np.random.choice(
    room_types,
    size=N,
    p=[0.45, 0.25, 0.20, 0.10]
)


treatment_cost = np.random.randint(
    5000,
    250000,
    N
)

insurance_coverage = np.round(
    treatment_cost *
    np.random.uniform(0.30, 0.90, N),
    2
)

patient_payment = np.round(
    treatment_cost - insurance_coverage,
    2
)

readmission = np.random.choice(
    ["Yes", "No"],
    size=N,
    p=[0.12, 0.88]
)


patient_satisfaction = np.random.randint(
    1,
    6,
    N
)

df = pd.DataFrame({

    "Patient_ID": patient_ids,

    "Admission_ID": admission_ids,

    "Admission_Date": admission_dates,

    "Discharge_Date": discharge_dates,

    "Age": ages,

    "Gender": gender_data,

    "City": city_data,

    "Department": department_data,

    "Admission_Type": admission_type_data,

    "Diagnosis": diagnosis_data,

    "Treatment": treatment_data,

    "Doctor_ID": doctor_ids,

    "Room_Type": room_data,

    "Length_of_Stay": length_of_stay,

    "Treatment_Cost": treatment_cost,

    "Insurance_Coverage": insurance_coverage,

    "Patient_Payment": patient_payment,

    "Readmission": readmission,

    "Patient_Satisfaction": patient_satisfaction
})

missing_columns = [
    "City",
    "Diagnosis",
    "Patient_Satisfaction"
]

for column in missing_columns:

    missing_indices = np.random.choice(
        df.index,
        size=int(N * 0.01),
        replace=False
    )

    df.loc[missing_indices, column] = np.nan

duplicates = df.sample(
    100,
    random_state=42
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

from pathlib import Path

# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Create data/raw folder automatically
raw_folder = project_folder / "data" / "raw"
raw_folder.mkdir(parents=True, exist_ok=True)

# Output file
output_path = raw_folder / "healthcare_patient_data.csv"

# Save dataset
df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Saved to: {output_path}")