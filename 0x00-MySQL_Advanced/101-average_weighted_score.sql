-- Script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes & stores the avg weighted score for all students
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS Usr, 
        (SELECT Usr.id, SUM(score * weight) / SUM(weight) AS w_avg 
        FROM users AS Usr 
        JOIN corrections as C ON Usr.id=C.user_id 
        JOIN projects AS P ON C.project_id=P.id 
        GROUP BY Usr.id)
    AS WAV
    SET Usr.average_score = WAV.w_avg 
    WHERE Usr.id=WAV.id;
END
$$
DELIMITER ;
