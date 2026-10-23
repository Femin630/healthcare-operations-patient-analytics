USE healthcare_analytics;

SELECT COUNT(*) AS total_rows
FROM healthcare_analytics.healthcare_patient_data_cleaned;

SELECT
    Department,
    COUNT(*) AS Patient_Count
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Department
ORDER BY Patient_Count DESC;

-- 3. Department financial analysis

SELECT
    Department,
    COUNT(*) AS Patient_Count,
    ROUND(SUM(Treatment_Cost), 2) AS Total_Treatment_Cost,
    ROUND(AVG(Treatment_Cost), 2) AS Average_Treatment_Cost,
    ROUND(SUM(Insurance_Coverage), 2) AS Total_Insurance,
    ROUND(SUM(Patient_Payment), 2) AS Total_Patient_Payment
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Department
ORDER BY Total_Treatment_Cost DESC;

-- 4. Monthly admission trend

SELECT
    DATE_FORMAT(Admission_Date, '%Y-%m') AS Admission_Month,
    COUNT(*) AS Total_Admissions
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY DATE_FORMAT(Admission_Date, '%Y-%m')
ORDER BY Admission_Month;

-- 5. Readmission rate by department

SELECT
    Department,
    COUNT(*) AS Total_Records,
    SUM(
        CASE WHEN Readmission = 'Yes' THEN 1 ELSE 0 END
    ) AS Readmitted_Records,
    ROUND(
        100.0 * SUM(
            CASE WHEN Readmission = 'Yes' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS Readmission_Percentage
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Department
ORDER BY Readmission_Percentage DESC;

-- 6. Top 10 Diagnoses

SELECT
    Diagnosis,
    COUNT(*) AS Patient_Count
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Diagnosis
ORDER BY Patient_Count DESC
LIMIT 10;

-- 7. City-wise Patient Volume

SELECT
    City,
    COUNT(*) AS Patient_Count
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY City
ORDER BY Patient_Count DESC;

-- 8. Patient Satisfaction by Department

SELECT
    Department,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(Patient_Satisfaction), 2) AS Average_Satisfaction
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Department
ORDER BY Average_Satisfaction DESC;

-- 9. Insurance Coverage Analysis

SELECT
    ROUND(SUM(Treatment_Cost), 2) AS Total_Treatment_Cost,
    ROUND(SUM(Insurance_Coverage), 2) AS Total_Insurance,
    ROUND(SUM(Patient_Payment), 2) AS Total_Patient_Payment,
    ROUND(
        100.0 * SUM(Insurance_Coverage)
        / NULLIF(SUM(Treatment_Cost), 0),
        2
    ) AS Insurance_Coverage_Percentage
FROM healthcare_analytics.healthcare_patient_data_cleaned;

-- 10. Treatment Cost Categories

SELECT
    CASE
        WHEN Treatment_Cost < 10000 THEN 'Low Cost'
        WHEN Treatment_Cost < 30000 THEN 'Medium Cost'
        ELSE 'High Cost'
    END AS Cost_Category,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(Treatment_Cost), 2) AS Average_Cost
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Cost_Category
ORDER BY Average_Cost;
-- 11. Department with Highest Total Treatment Cost

SELECT
    Department,
    Total_Cost
FROM (
    SELECT
        Department,
        SUM(Treatment_Cost) AS Total_Cost
    FROM healthcare_analytics.healthcare_patient_data_cleaned
    GROUP BY Department
) AS Department_Summary
WHERE Total_Cost = (
    SELECT MAX(Total_Cost)
    FROM (
        SELECT SUM(Treatment_Cost) AS Total_Cost
        FROM healthcare_analytics.healthcare_patient_data_cleaned
        GROUP BY Department
    ) AS Department_Totals
);

-- 12. Department Performance Using CTE

WITH Department_Performance AS (
    SELECT
        Department,
        COUNT(*) AS Patient_Count,
        ROUND(AVG(Length_of_Stay), 2) AS Average_LOS,
        ROUND(AVG(Patient_Satisfaction), 2) AS Average_Satisfaction,
        ROUND(AVG(Treatment_Cost), 2) AS Average_Treatment_Cost
    FROM healthcare_analytics.healthcare_patient_data_cleaned
    GROUP BY Department
)
SELECT *
FROM Department_Performance
ORDER BY Patient_Count DESC;

-- 13. Rank Departments by Total Treatment Cost

SELECT
    Department,
    Total_Treatment_Cost,
    RANK() OVER (
        ORDER BY Total_Treatment_Cost DESC
    ) AS Department_Rank
FROM (
    SELECT
        Department,
        SUM(Treatment_Cost) AS Total_Treatment_Cost
    FROM healthcare_analytics.healthcare_patient_data_cleaned
    GROUP BY Department
) AS Department_Costs;

-- 14. Overall Healthcare KPIs

SELECT
    COUNT(*) AS Total_Records,
    ROUND(AVG(Age), 2) AS Average_Age,
    ROUND(AVG(Length_of_Stay), 2) AS Average_LOS,
    ROUND(SUM(Treatment_Cost), 2) AS Total_Treatment_Cost,
    ROUND(AVG(Patient_Satisfaction), 2) AS Average_Satisfaction,
    SUM(CASE WHEN Readmission = 'Yes' THEN 1 ELSE 0 END)
        AS Total_Readmissions
FROM healthcare_analytics.healthcare_patient_data_cleaned;

-- 15. Admission Type Analysis

SELECT
    Admission_Type,
    COUNT(*) AS Total_Admissions,
    ROUND(AVG(Length_of_Stay), 2) AS Average_LOS,
    ROUND(AVG(Treatment_Cost), 2) AS Average_Cost
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Admission_Type
ORDER BY Total_Admissions DESC;

-- 16. Gender-wise Patient Analysis

SELECT
    Gender,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(Age), 2) AS Average_Age,
    ROUND(AVG(Treatment_Cost), 2) AS Average_Treatment_Cost
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Gender
ORDER BY Patient_Count DESC;

-- 17. Length of Stay Analysis

SELECT
    CASE
        WHEN Length_of_Stay <= 3 THEN 'Short Stay'
        WHEN Length_of_Stay <= 7 THEN 'Medium Stay'
        ELSE 'Long Stay'
    END AS Stay_Category,
    COUNT(*) AS Patient_Count,
    ROUND(AVG(Treatment_Cost), 2) AS Average_Treatment_Cost
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Stay_Category
ORDER BY Patient_Count DESC;

-- 18. Patient Payment vs Treatment Cost

SELECT
    Department,
    ROUND(SUM(Treatment_Cost), 2) AS Total_Treatment_Cost,
    ROUND(SUM(Insurance_Coverage), 2) AS Total_Insurance,
    ROUND(SUM(Patient_Payment), 2) AS Total_Patient_Payment,
    ROUND(
        100.0 * SUM(Patient_Payment)
        / NULLIF(SUM(Treatment_Cost), 0),
        2
    ) AS Patient_Payment_Percentage
FROM healthcare_analytics.healthcare_patient_data_cleaned
GROUP BY Department
ORDER BY Patient_Payment_Percentage DESC;