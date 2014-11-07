drop table student;
drop table instructor;
drop table takes;
drop table teaches;

create table student
	(roll			varchar(10), 
	 name			varchar(20), 
	 department		varchar(20), 
	 credits		INT,
	 hometown    	varchar(40),
	 hostel         INT
);
create table takes
	(roll           varchar(10),
	 course 		varchar(40),
	 year  			INT,
	 semester		varchar(30),
	 grade			varchar(1)
);
create table instructor
	(id				varchar(10), 
	 name			varchar(20), 
	 department		varchar(20), 
	 salary			INT,
	 hometown       varchar(40),
	 office         varchar(100)
);
create table teaches
	(id           	varchar(10),
	 course 		varchar(40),
	 year  			INT,
	 semester		varchar(30)
);