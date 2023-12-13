-- Script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes & stores the avg  weighted score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    user_id INT
)
BEGIN
    DECLARE wght_avg_score FLOAT;
    SET wght_avg_score = (SELECT SUM(score * weight) / SUM(weight) 
                        FROM users AS Usr 
                        JOIN corrections as C ON Usr.id=C.user_id 
                        JOIN projects AS P ON C.project_id=P.id 
                        WHERE Usr.id=user_id);
    UPDATE users SET average_score = wght_avg_score WHERE id=user_id;
END
$$
DELIMITER ;
