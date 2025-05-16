-- tuberculosis_analysis.sql
-- SQL analysis of the ‘xray_data’ medical dataset

-- 1. Total number of patients
-- Answer : 20000

SELECT COUNT(*) AS total_patients
FROM xray_data;

-- 2. Class distribution (Normal vs Tuberculosis)
-- Nomal : 14082 / Tuberculosis : 5918

SELECT Class, COUNT(*) AS nombre_de_cas
FROM xray_data
GROUP BY Class;

-- 3. Distribution of Patient by gender and Classes
-- Female	Normal :	6877
--Female	Tuberculosis : 2952
--Male	Normal	: 7205
--Male	Tuberculosis	: 2966

SELECT Gender, Class, COUNT(*) AS nb
FROM xray_data
GROUP BY Gender, Class
ORDER BY Gender, Class;

-- 4. Average age of patients, by type of diagnosis
-- Normal : 53.4 years
-- Tuberculosi : 53.6 years

SELECT Class, ROUND(AVG(Age), 1) AS age_moyen
FROM xray_data
GROUP BY Class;

-- 5. Distribution of fever types by class
-- High	Normal	4624
-- High	Tuberculosis	1962
-- Mild	Normal	4663
-- Mild	Tuberculosis	2038
-- Moderate	Normal	4795
-- Moderate	Tuberculosis	1918

SELECT Fever, Class, COUNT(*) AS nb
FROM xray_data
GROUP BY Fever, Class
ORDER BY Fever, Class;

-- 6. Tuberculosis with severe breathlessness (Breathlessness >= 4) and Cought severity (Cough_Severity >=5)
-- PID000025	79	Male	No	7	4	0	6.36	High	Yes	High	Yes	Former	Yes	Tuberculosis
-- PID000044	77	Female	Yes	9	4	3	10.78	High	No	High	Yes	Current	No	Tuberculosis
-- PID000090	45	Female	Yes	7	4	0	8.63	High	Yes	High	Yes	Former	No	Tuberculosis
-- PID000129	79	Female	No	7	4	1	10.62	Mild	Yes	Medium	Yes	Never	Yes	Tuberculosis
-- PID000142	87	Male	No	9	4	5	14.22	Mild	Yes	Low	No	Former	Yes	Tuberculosis


SELECT *
FROM xray_data
WHERE Class = 'Tuberculosis' AND Breathlessness >= 4 AND Cough_Severity >=5
LIMIT 5;

-- 7. Impact of smoking on cases of tuberculosis
-- Current	Normal	4674
-- Current	Tuberculosis	1919
-- Former	Normal	4751
-- Former	Tuberculosis	2040
-- Never	Normal	4657
-- Never	Tuberculosis	1959

SELECT Smoking_History, Class, COUNT(*) AS nb
FROM xray_data
GROUP BY Smoking_History, Class
ORDER BY Smoking_History, Class;

-- 8. Patients with blood in sputum
-- 9925 patients with blood in sputum

SELECT COUNT(*) AS nb_patients_avec_sang
FROM xray_data
WHERE Blood_in_Sputum = 'Yes';

-- 9. History of TB and current diagnosis
-- No	Normal	6991
-- No	Tuberculosis	2942
-- Yes	Normal	7091
-- Yes	Tuberculosis	2976

SELECT Previous_TB_History, Class, COUNT(*) AS nb
FROM xray_data
GROUP BY Previous_TB_History, Class
ORDER BY Previous_TB_History, Class;

-- 10. Average symptom scores by diagnosis
-- Normal	Avg_cough : 4.49 / Avg_breathlessness :	2.0	/ Avg_fatigue : 4.52	/ Avg_weight_loss : 7.45
-- Tuberculosis	Avg_cough : 4.5	/ Avg_breathlessness :2.01 / Avg_fatigue :	4.47 / Avg_weight_loss :	7.47

SELECT 
  Class,
  ROUND(AVG(Cough_Severity), 2) AS avg_cough,
  ROUND(AVG(Breathlessness), 2) AS avg_breathlessness,
  ROUND(AVG(Fatigue), 2) AS avg_fatigue,
  ROUND(AVG(Weight_Loss), 2) AS avg_weight_loss
FROM xray_data
GROUP BY Class;

-- 11. Cough_Severity vs Class (Couhg_Severity / tb_casse s/ normal/cases)
-- 0	593	1398
-- 1	595	1406
-- 2	591	1430
-- 3	599	1397
-- 4	604	1398
-- 5	571	1466
-- 6	592	1394
-- 7	568	1402
-- 8	609	1458
-- 9	596	1333

SELECT 
  Cough_Severity,
  SUM(CASE WHEN Class = 'Tuberculosis' THEN 1 ELSE 0 END) AS tb_cases,
  SUM(CASE WHEN Class = 'Normal' THEN 1 ELSE 0 END) AS normal_cases
FROM xray_data
GROUP BY Cough_Severity
ORDER BY Cough_Severity;

-- 12. Breathlessness vs Class (Breathlessness / tb_ratio)
-- 0	0.29
-- 1	0.298
-- 2	0.296
-- 3	0.298
-- 4	0.298

SELECT 
  Breathlessness,
  ROUND(AVG(CASE WHEN Class = 'Tuberculosis' THEN 1 ELSE 0 END), 3) AS tb_ratio
FROM xray_data
GROUP BY Breathlessness
ORDER BY Breathlessness;

-- 13. Fever level vs Class
-- High	Normal	4624
-- High	Tuberculosis	1962
-- Mild	Normal	4663
-- Mild	Tuberculosis	2038
-- Moderate	Normal	4795
-- Moderate	Tuberculosis	1918

SELECT 
  Fever,
  Class,
  COUNT(*) AS nb
FROM xray_data
GROUP BY Fever, Class
ORDER BY Fever, Class;

-- 14. History of TB vs. current diagnosis 
-- No	Normal	6991
-- No	Tuberculosis	2942
-- Yes	Normal	7091
-- Yes	Tuberculosis	2976

SELECT 
  Previous_TB_History,
  Class,
  COUNT(*) AS nb
FROM xray_data
GROUP BY Previous_TB_History, Class
ORDER BY Previous_TB_History, Class;

-- 15. Correlation between smoking and TB ? (Smoking_History and tb_ratio)
-- Current	0.291
-- Former	0.3
-- Never	0.296

SELECT 
  Smoking_History,
  ROUND(AVG(CASE WHEN Class = 'Tuberculosis' THEN 1 ELSE 0 END), 3) AS tb_ratio
FROM xray_data
GROUP BY Smoking_History;

-- 16. Correlation between high fatigue and TB ? (Fatigue / total / tb_cases / tb_ratio)
-- 0	2036	606	0.3
-- 1	1999	632	0.32
-- 2	1976	568	0.29
-- 3	1955	562	0.29
-- 4	1997	603	0.3
-- 5	1945	585	0.3
-- 6	2026	603	0.3
-- 7	2047	604	0.3
-- 8	2016	568	0.28
-- 9	2003	587	0.29

SELECT 
  Fatigue,
  COUNT(*) AS total,
  SUM(CASE WHEN Class = 'Tuberculosis' THEN 1 ELSE 0 END) AS tb_cases,
  ROUND(1.0 * SUM(CASE WHEN Class = 'Tuberculosis' THEN 1 ELSE 0 END) / COUNT(*), 2) AS tb_ratio
FROM xray_data
GROUP BY Fatigue
ORDER BY Fatigue;

-- End of the note.