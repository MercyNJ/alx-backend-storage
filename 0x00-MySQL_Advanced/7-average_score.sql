--  creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average score for a student
-- Create a stored procedure ComputeAverageScoreForUser
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE calculated_average FLOAT;

    SET calculated_average = (SELECT AVG(score) FROM corrections AS cor WHERE cor.user_id = user_id);

    UPDATE users
    SET average_score = IFNULL(calculated_average, 0)
    WHERE id = user_id;
END $$
DELIMITER ;
