-- creates a function SafeDiv that divides (and returns) the 1rst
-- by the 2nd num or returns 0 if 2nd number is equal to 0
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    IF (b = 0)
    THEN
        RETURN (0);
    ELSE
        RETURN (a / b);
    END IF;
END
$$
DELIMITER ;
