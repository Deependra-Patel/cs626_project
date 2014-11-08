









SELECT T1.name FROM ( SELECT * FROM instructor NATURAL JOIN teaches ) AS T1 WHERE T1.course = 'CS626' ;
SELECT T1.name FROM instructor AS T1 WHERE T1.department = 'CS' ;

SELECT T1.name FROM instructor AS T1 WHERE T1.salary > 20000 and T1.department != 'mechanical' ;
