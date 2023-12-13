-- script that creates a view need_meeting listing all
-- students with a  score under 80 (strict) & 
-- no last_meeting or more than 1 month
CREATE VIEW need_meeting AS 
SELECT name FROM students 
WHERE 
    score < 80 AND 
    (last_meeting IS NULL 
        OR 
    last_meeting < ADDDATE(CURDATE(), interval -1 MONTH));
