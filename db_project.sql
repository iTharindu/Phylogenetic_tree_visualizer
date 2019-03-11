Drop DATABASE if EXISTS db_phygraph ;

Create DATABASE db_phygraph ;

create table Users(
    user_id int(12) AUTO_INCREMENT primary key,
    user_name varchar(50) not null,
    user_email varchar(100) not null,
    password VARCHAR(100) not null
);