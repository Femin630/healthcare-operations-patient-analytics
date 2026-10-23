
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Healthcare Analytics",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Operations & Patient Analytics")
st.caption("Interactive dashboard | Synthetic healthcare dataset")

# Locate the cleaned CSV file
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "cleaned"
    / "healthcare_patient_data_cleaned.csv"
)

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df["Admission_Date"] = pd.to_datetime(
        df["Admission_Date"], errors="coerce"
    )
    return df

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info(
        "Check that the cleaned CSV is inside "
        "data/cleaned/ in your main project folder."
    )
    st.stop()

df = load_data(str(DATA_FILE))

# Sidebar filters
st.sidebar.header("Dashboard Filters")

departments = sorted(df["Department"].dropna().unique())
selected_departments = st.sidebar.multiselect(
    "Select Department",
    departments,
    default=departments
)

filtered = df[df["Department"].isin(selected_departments)].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Patient Records", f"{len(filtered):,}")
c2.metric(
    "Average Length of Stay",
    f"{filtered['Length_of_Stay'].mean():.2f} days"
)
c3.metric(
    "Total Treatment Cost",
    f"₹{filtered['Treatment_Cost'].sum():,.0f}"
)
c4.metric(
    "Average Satisfaction",
    f"{filtered['Patient_Satisfaction'].mean():.2f} / 5"
)

st.divider()

# Department analysis
left, right = st.columns(2)

with left:
    st.subheader("Patients by Department")
    dept_counts = (
        filtered.groupby("Department")
        .size()
        .reset_index(name="Patient_Count")
        .sort_values("Patient_Count", ascending=False)
    )
    fig = px.bar(
        dept_counts,
        x="Department",
        y="Patient_Count",
        title="Department-wise Patient Count",
        text="Patient_Count"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Monthly Admissions")
    monthly = (
        filtered.dropna(subset=["Admission_Date"])
        .assign(
            Admission_Month=lambda x:
                x["Admission_Date"].dt.to_period("M").astype(str)
        )
        .groupby("Admission_Month")
        .size()
        .reset_index(name="Admissions")
        .sort_values("Admission_Month")
    )
    fig = px.line(
        monthly,
        x="Admission_Month",
        y="Admissions",
        markers=True,
        title="Monthly Admission Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# Readmission and admission type
left, right = st.columns(2)

with left:
    st.subheader("Readmission Distribution")
    readmission = (
        filtered["Readmission"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Readmission")
        .reset_index(name="Records")
    )
    fig = px.pie(
        readmission,
        names="Readmission",
        values="Records",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Admission Type")
    admission_types = (
        filtered["Admission_Type"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Admission_Type")
        .reset_index(name="Records")
    )
    fig = px.bar(
        admission_types,
        x="Admission_Type",
        y="Records",
        title="Records by Admission Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# Satisfaction analysis
st.subheader("Average Patient Satisfaction by Department")
satisfaction = (
    filtered.groupby("Department", as_index=False)
    ["Patient_Satisfaction"].mean()
)
satisfaction["Patient_Satisfaction"] = (
    satisfaction["Patient_Satisfaction"].round(2)
)

fig = px.bar(
    satisfaction,
    x="Department",
    y="Patient_Satisfaction",
    range_y=[0, 5],
    title="Average Satisfaction Score"
)
st.plotly_chart(fig, use_container_width=True)

# Data preview and download
with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="healthcare_filtered_data.csv",
    mime="text/csv"
)

st.caption(
    "Portfolio project using synthetic data for educational purposes. "
    "Results do not represent real patients."
)
