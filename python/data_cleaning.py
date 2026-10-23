import pandas as pd
from pathlib import Path

# Project folder
project_folder = Path(__file__).resolve().parent.parent

# Raw dataset path
file_path = project_folder / "data" / "raw" / "healthcare_patient_data.csv"

# Load dataset
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

duplicates_removed = before_duplicates - after_duplicates

print("\n DUPLICATE CLEANING ")
print("Rows before removing duplicates:", before_duplicates)
print("Duplicate rows removed:", duplicates_removed)
print("Rows after removing duplicates:", after_duplicates)



missing_count = df.isnull().sum()

missing_percentage = (
    missing_count / len(df) * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage
})

print("\n MISSING VALUE SUMMARY ")
print(missing_summary[missing_summary["Missing_Count"] > 0])


# Fill missing City values with the most frequent city
city_mode = df["City"].mode()[0]

df["City"] = df["City"].fillna(city_mode)

print("\nCity missing values after cleaning:")
print(df["City"].isnull().sum())

# Fill missing Diagnosis values with the most frequent diagnosis
diagnosis_mode = df["Diagnosis"].mode()[0]

df["Diagnosis"] = df["Diagnosis"].fillna(diagnosis_mode)

print("\nDiagnosis missing values after cleaning:")
print(df["Diagnosis"].isnull().sum())

# Fill missing Patient Satisfaction values with the median
satisfaction_median = df["Patient_Satisfaction"].median()

df["Patient_Satisfaction"] = df[
    "Patient_Satisfaction"
].fillna(satisfaction_median)

print("\nPatient Satisfaction missing values after cleaning:")
print(df["Patient_Satisfaction"].isnull().sum())

print("\n FINAL MISSING VALUE CHECK ")

print(df.isnull().sum())


cleaned_folder = project_folder / "data" / "cleaned"
cleaned_folder.mkdir(parents=True, exist_ok=True)

cleaned_file_path = cleaned_folder / "healthcare_patient_data_cleaned.csv"

df.to_csv(cleaned_file_path, index=False)

print("\n CLEANED DATASET SAVED ")
print("Cleaned dataset saved successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("File:", cleaned_file_path)


# Convert date columns to datetime format

df["Admission_Date"] = pd.to_datetime(df["Admission_Date"])
df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"])

print("\n Date Column Check")
print("Admission_Date type:", df["Admission_Date"].dtype)
print("Discharge_Date type:", df["Discharge_Date"].dtype)



# Validate Length of Stay
calculated_los = (
    df["Discharge_Date"] - df["Admission_Date"]
).dt.days

los_difference = df["Length_of_Stay"] - calculated_los

print("\n Length of stay")
print("Maximum difference:", los_difference.abs().max())
print("Rows with mismatch:", (los_difference != 0).sum())


# Check for invalid Length of Stay values
invalid_los = df[df["Length_of_Stay"] <= 0]

print("\n Stay chek of invalid")
print("Invalid Length of Stay rows:", len(invalid_los))


# Check for invalid Treatment Cost values
invalid_cost = df[df["Treatment_Cost"] <= 0]

print("\n Invalide Treatment cost")
print("Invalid Treatment Cost rows:", len(invalid_cost))

# Check for invalid Insurance Coverage values

invalid_insurance = df[df["Insurance_Coverage"] < 0]

print("\n Invalid insurance coverage")
print("Invalid Insurance Coverage rows:", len(invalid_insurance))


# Check for invalid Patient Payment values
invalid_payment = df[df["Patient_Payment"] < 0]

print("\n Patient Payment Check")
print("Invalid Patient Payment rows:", len(invalid_payment))

# Validate Treatment Cost against Insurance Coverage and Patient Payment

calculated_total = (
    df["Insurance_Coverage"] + df["Patient_Payment"]
)

payment_difference = (
    df["Treatment_Cost"] - calculated_total
)

print("\n Payment Validation")
print("Maximum difference:", payment_difference.abs().max())
print("Rows with mismatch:", (payment_difference != 0).sum())



# Check for invalid Age values
invalid_age = df[
    (df["Age"] < 0) | (df["Age"] > 120)
]
print("\n Check Invalid Age")
print("Invalid Age rows:", len(invalid_age))


# Check for invalid Patient Satisfaction values

invalid_satisfaction = df[
    (df["Patient_Satisfaction"] < 1) |
    (df["Patient_Satisfaction"] > 5)
]

print("\n Invalida Patient Satisfaction Check")
print("Invalid Patient Satisfaction rows:", len(invalid_satisfaction))

# Check unique Gender values
print("\n Gender Value")
print(df["Gender"].value_counts(dropna=False))

# Check unique Department values
print("\n Department Value")
print(df["Department"].value_counts(dropna=False))

# Check unique Admission Type values
print("\n Admission type value")
print(df["Admission_Type"].value_counts(dropna=False))

# Check unique Treatment values
print("\n Treatment Value")
print(df["Treatment"].value_counts(dropna=False))

# Check unique Room Type values
print("\n Roome Type Value")
print(df["Room_Type"].value_counts(dropna=False))   

# Check unique Readmission values
print("\n Readmission value")
print(df["Readmission"].value_counts(dropna=False))

# Check unique City values
print("\n City Value")
print(df["City"].value_counts(dropna=False))

print("\n\n ")
print("FINAL DATA QUALITY CHECKS")
print(" ")

# 1. City values
print("\n CITY VALUES ")
print(df["City"].value_counts(dropna=False))

# 2. Diagnosis values
print("\n DIAGNOSIS VALUES ")
print(df["Diagnosis"].value_counts(dropna=False))

# 3. Admission Type values
print("\n ADMISSION TYPE VALUES ")
print(df["Admission_Type"].value_counts(dropna=False))

# 4. Treatment values
print("\n TREATMENT VALUES ")
print(df["Treatment"].value_counts(dropna=False))

# 5. Room Type values
print("\n ROOM TYPE VALUES ")
print(df["Room_Type"].value_counts(dropna=False))

# 6. Readmission values
print("\n READMISSION VALUES")
print(df["Readmission"].value_counts(dropna=False))

# 7. Gender values
print("\n GENDER VALUES")
print(df["Gender"].value_counts(dropna=False))


print("\n FINAL MISSING VALUE CHECK ")
print(df.isnull().sum())

print("\n FINAL DUPLICATE CHECK")
print("Duplicate rows:", df.duplicated().sum())

print("\n  FINAL DATASET SHAPE ")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\n NUMERICAL VALIDATION ")

print(
    "Invalid Age:",
    len(df[(df["Age"] < 0) | (df["Age"] > 120)])
)

print(
    "Invalid Length of Stay:",
    len(df[df["Length_of_Stay"] <= 0])
)

print(
    "Invalid Treatment Cost:",
    len(df[df["Treatment_Cost"] <= 0])
)

print(
    "Invalid Insurance Coverage:",
    len(df[df["Insurance_Coverage"] < 0])
)

print(
    "Invalid Patient Payment:",
    len(df[df["Patient_Payment"] < 0])
)

print(
    "Invalid Patient Satisfaction:",
    len(
        df[
            (df["Patient_Satisfaction"] < 1)
            | (df["Patient_Satisfaction"] > 5)
        ]
    )
)

calculated_total = (
    df["Insurance_Coverage"] +
    df["Patient_Payment"]
)

financial_difference = (
    df["Treatment_Cost"] -
    calculated_total
)

print("\n FINANCIAL CONSISTENCY")
print(
    "Financial mismatches:",
    (financial_difference != 0).sum()
)

calculated_los = (
    df["Discharge_Date"] -
    df["Admission_Date"]
).dt.days

los_difference = (
    df["Length_of_Stay"] -
    calculated_los
)

print("\n DATE CONSISTENCY")
print(
    "Length of Stay mismatches:",
    (los_difference != 0).sum()
)

cleaned_folder = project_folder / "data" / "cleaned"
cleaned_folder.mkdir(parents=True, exist_ok=True)

cleaned_file_path = (
    cleaned_folder /
    "healthcare_patient_data_cleaned.csv"
)

df.to_csv(
    cleaned_file_path,
    index=False
)

print("\n ")
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("")

print("Final Rows:", df.shape[0])
print("Final Columns:", df.shape[1])
print("Saved File:", cleaned_file_path)