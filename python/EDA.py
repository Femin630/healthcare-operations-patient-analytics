import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

#Load Dataset

project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder
    / "data"
    / "cleaned"
    / "healthcare_patient_data_cleaned.csv"
)

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

# Convert date columns
df["Admission_Date"] = pd.to_datetime(df["Admission_Date"])
df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"])


print("\n DATASET OVERVIEW")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

total_patients = df["Patient_ID"].nunique()
average_age = df["Age"].mean()
average_length_of_stay = df["Length_of_Stay"].mean()
total_treatment_cost = df["Treatment_Cost"].sum()
average_treatment_cost = df["Treatment_Cost"].mean()
total_insurance_coverage = df["Insurance_Coverage"].sum()
total_patient_payment = df["Patient_Payment"].sum()
average_patient_satisfaction = df["Patient_Satisfaction"].mean()


print("\n Overall Helathcare KPI")

print("Total Patients:", total_patients)

print("Average Patient Age:", round(average_age, 2))

print(
    "Average Length of Stay:",
    round(average_length_of_stay, 2),
    "days"
)

print(
    "Total Treatment Cost:",
    round(total_treatment_cost, 2)
)

print(
    "Average Treatment Cost:",
    round(average_treatment_cost, 2)
)

print(
    "Total Insurance Coverage:",
    round(total_insurance_coverage, 2)
)

print(
    "Total Patient Payment:",
    round(total_patient_payment, 2)
)

print(
    "Average Patient Satisfaction:",
    round(average_patient_satisfaction, 2),
    "/ 5"
)
department_patients = (
    df["Department"]
    .value_counts()
    .reset_index()
)

department_patients.columns = [
    "Department",
    "Patient_Count"
]

print("\n Department vise patient count")
print(department_patients)


plt.figure(figsize=(10, 6))

bars = plt.bar(
    department_patients["Department"],
    department_patients["Patient_Count"]
)

plt.title("Patient Volume by Department")
plt.xlabel("Department")
plt.ylabel("Number of Patients")

plt.xticks(rotation=45)

# Show exact patient count on each bar
for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 20,
        str(int(height)),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

# monthly admission analysis
df["Admission_Month"] = df["Admission_Date"].dt.to_period("M")

monthly_admissions = (
    df.groupby("Admission_Month")
    .size()
    .reset_index(name="Patient_Count")
)

monthly_admissions["Admission_Month"] = (
    monthly_admissions["Admission_Month"]
    .astype(str)
)

print("\n Monthly admission")
print(monthly_admissions)

# Monthly admission chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_admissions["Admission_Month"],
    monthly_admissions["Patient_Count"],
    marker="o"
)

plt.title("Monthly Patient Admission Trend")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

admission_type = (
    df["Admission_Type"]
    .value_counts()
    .reset_index()
)

admission_type.columns = [
    "Admission_Type",
    "Patient_Count"
]

print("\n Admission type analysis")
print(admission_type)

# ============================================================
# ADMISSION TYPE PERCENTAGE ANALYSIS
# ============================================================

admission_type_percentage = (
    df["Admission_Type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index()
)

admission_type_percentage.columns = [
    "Admission_Type",
    "Percentage"
]

print("\n========== ADMISSION TYPE PERCENTAGE ==========")
print(admission_type_percentage)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    admission_type_percentage["Admission_Type"],
    admission_type_percentage["Percentage"]
)

plt.title("Admission Type Distribution")
plt.xlabel("Admission Type")
plt.ylabel("Percentage (%)")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.1f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

# ============================================================
# DEPARTMENT-WISE LENGTH OF STAY
# ============================================================

department_los = (
    df.groupby("Department")["Length_of_Stay"]
    .mean()
    .round(2)
    .reset_index()
)

department_los.columns = [
    "Department",
    "Average_Length_of_Stay"
]

department_los = department_los.sort_values(
    "Average_Length_of_Stay",
    ascending=False
)

print("\n Average lenght of stay")
print(department_los)


department_cost = (
    df.groupby("Department")["Treatment_Cost"]
    .agg(
        Total_Treatment_Cost="sum",
        Average_Treatment_Cost="mean"
    )
    .round(2)
    .reset_index()
)

department_cost = department_cost.sort_values(
    "Total_Treatment_Cost",
    ascending=False
)

print("\n Department vise Treatment cost")
print(department_cost)

# ============================================================
# AVERAGE LENGTH OF STAY CHART
# ============================================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    department_los["Department"],
    department_los["Average_Length_of_Stay"]
)

plt.title("Average Length of Stay by Department")
plt.xlabel("Department")
plt.ylabel("Average Length of Stay (Days)")
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.05,
        f"{height:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
bars = plt.bar(
    department_cost["Department"],
    department_cost["Total_Treatment_Cost"]
)

plt.title("Total Treatment Cost by Department")
plt.xlabel("Department")
plt.ylabel("Total Treatment Cost")
plt.xticks(rotation=45)

plt.ticklabel_format(
    style="plain",
    axis="y"
)

plt.tight_layout()
plt.show()

top_diagnoses = (
    df["Diagnosis"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_diagnoses.columns = [
    "Diagnosis",
    "Patient_Count"
]

print("\n Top 10 Diagnoses")
print(top_diagnoses)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    top_diagnoses["Diagnosis"],
    top_diagnoses["Patient_Count"]
)

plt.title("Top 10 Diagnoses by Patient Count")
plt.xlabel("Diagnosis")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 10,
        str(int(height)),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

readmission_count = (
    df["Readmission"]
    .value_counts()
    .reset_index()
)

readmission_count.columns = [
    "Readmission",
    "Patient_Count"
]

print("\n========== READMISSION ANALYSIS ==========")
print(readmission_count)

readmission_rate = (
    df["Readmission"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\n Readmisson Rate")

for category, percentage in readmission_rate.items():
    print(
        f"{category}: {percentage}%"
    )

plt.figure(figsize=(7, 5))

bars = plt.bar(
    readmission_count["Readmission"],
    readmission_count["Patient_Count"]
)

plt.title("Patient Readmission Distribution")
plt.xlabel("Readmission")
plt.ylabel("Number of Patients")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 50,
        str(int(height)),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

financial_summary = (
    df.groupby("Department")
    .agg(
        Total_Treatment_Cost=("Treatment_Cost", "sum"),
        Total_Insurance_Coverage=("Insurance_Coverage", "sum"),
        Total_Patient_Payment=("Patient_Payment", "sum"),
        Average_Treatment_Cost=("Treatment_Cost", "mean")
    )
    .round(2)
    .reset_index()
)

financial_summary = financial_summary.sort_values(
    "Total_Treatment_Cost",
    ascending=False
)

print("\n Financial analysis")
print(financial_summary)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    financial_summary["Department"],
    financial_summary["Total_Treatment_Cost"]
)

plt.title("Total Treatment Cost by Department")
plt.xlabel("Department")
plt.ylabel("Total Treatment Cost")
plt.xticks(rotation=45)

plt.ticklabel_format(
    style="plain",
    axis="y"
)

plt.tight_layout()
plt.show()

city_patients = (
    df["City"]
    .value_counts()
    .reset_index()
)

city_patients.columns = [
    "City",
    "Patient_Count"
]

print("\n Patient Count")
print(city_patients)


top_cities = city_patients.head(10)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    top_cities["City"],
    top_cities["Patient_Count"]
)

plt.title("Patient Volume by City")
plt.xlabel("City")
plt.ylabel("Number of Patients")

plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 20,
        str(int(height)),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 30, 45, 60, 120],
    labels=[
        "0-18",
        "19-30",
        "31-45",
        "46-60",
        "60+"
    ]
)

age_group_analysis = (
    df["Age_Group"]
    .value_counts()
    .sort_index()
    .reset_index()
)

age_group_analysis.columns = [
    "Age_Group",
    "Patient_Count"
]

print("\n Age group analysis")
print(age_group_analysis)

plt.figure(figsize=(9, 5))

bars = plt.bar(
    age_group_analysis["Age_Group"].astype(str),
    age_group_analysis["Patient_Count"]
)

plt.title("Patient Distribution by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Patients")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 50,
        str(int(height)),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

admission_department = pd.crosstab(
    df["Department"],
    df["Admission_Type"]
)

print("\n Admission type by department")
print(admission_department)

admission_department.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Admission Type Distribution by Department")
plt.xlabel("Department")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

readmission_department = (
    df.groupby("Department")["Readmission"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .round(2)
    .reset_index()
)

readmission_department.columns = [
    "Department",
    "Readmission_Rate"
]

readmission_department = readmission_department.sort_values(
    "Readmission_Rate",
    ascending=False
)

print("\n Readmission rate by department")
print(readmission_department)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    readmission_department["Department"],
    readmission_department["Readmission_Rate"]
)

plt.title("Readmission Rate by Department")
plt.xlabel("Department")
plt.ylabel("Readmission Rate (%)")
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f"{height:.2f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()

department_performance = (
    df.groupby("Department")
    .agg(
        Patient_Count=("Patient_ID", "nunique"),
        Average_LOS=("Length_of_Stay", "mean"),
        Average_Treatment_Cost=("Treatment_Cost", "mean"),
        Total_Treatment_Cost=("Treatment_Cost", "sum"),
        Average_Satisfaction=("Patient_Satisfaction", "mean")
    )
    .round(2)
    .reset_index()
)

department_performance = department_performance.sort_values(
    "Patient_Count",
    ascending=False
)

print("\n Department operational performance")
print(department_performance)


numeric_columns = [
    "Age",
    "Length_of_Stay",
    "Treatment_Cost",
    "Insurance_Coverage",
    "Patient_Payment",
    "Patient_Satisfaction"
]

correlation_matrix = df[numeric_columns].corr()

print("\n Correction Matrix")
print(correlation_matrix.round(2))

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f"
)

plt.title("Healthcare Dataset Correlation Matrix")

plt.tight_layout()
plt.show()

output_folder = project_folder / "data" / "eda_outputs"

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

# Save department performance
department_performance.to_csv(
    output_folder / "department_performance.csv",
    index=False
)

# Save monthly admissions
monthly_admissions.to_csv(
    output_folder / "monthly_admissions.csv",
    index=False
)

# Save admission type analysis
admission_type.to_csv(
    output_folder / "admission_type_analysis.csv",
    index=False
)

# Save readmission analysis
readmission_department.to_csv(
    output_folder / "readmission_by_department.csv",
    index=False
)


# Save top diagnoses
top_diagnoses.to_csv(
    output_folder / "top_diagnoses.csv",
    index=False
)


# Save financial analysis
financial_summary.to_csv(
    output_folder / "financial_summary.csv",
    index=False
)


print("\n====")
print("EDA ANALYSIS COMPLETED SUCCESSFULLY!")
print("======")

print("EDA output files saved to:")
print(output_folder)


