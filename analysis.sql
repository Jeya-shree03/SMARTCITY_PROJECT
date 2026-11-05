-- 1. Total complaints
SELECT COUNT(*) AS total_complaints
FROM complaints;

-- 2. Open complaints
SELECT COUNT(*) AS open_complaints
FROM complaints
WHERE complaint_status = 'Open';

-- 3. Closed complaints
SELECT COUNT(*) AS closed_complaints
FROM complaints
WHERE complaint_status = 'Closed';

-- 4. Top 10 complaint types
SELECT
    complaint_type,
    COUNT(*) AS total
FROM complaints
GROUP BY complaint_type
ORDER BY total DESC
LIMIT 10;

-- 5. Borough-wise complaints
SELECT
    borough,
    COUNT(*) AS total
FROM complaints
GROUP BY borough
ORDER BY total DESC;

-- 6. Agency-wise complaints
SELECT
    agency,
    COUNT(*) AS total
FROM complaints
GROUP BY agency
ORDER BY total DESC;