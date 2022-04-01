----------------------------------------------------------------
-- COSI 127B Assignment #1, Template for Answers to Question #2
----------------------------------------------------------------
-- Use CREATE TABLE statement to create tables for these eight relations. 
---------------------------------------------------------------
--a. FOREST (forest no, name, area, acid level, mbr xmin, mbr xmax, mbr ymin, mbr ymax) 
--     PK (forest no); 
-- [PASTE DDL BELOW]
---------------------------------------------------------------
create table forest (
    forest_no varchar(10),
    name varchar(30),
    area real,
    acid_level real,
    mbr_xmin real,
    mbr_xmax real,
    mbr_ymin real,
    mbr_ymax real,
    primary key (forest_no)
);

---------------------------------------------------------------
--b: STATE (name, abbreviation, area, population) 
--     PK (abbreviation); 
-- [PASTE DDL BELOW]
---------------------------------------------------------------
create table state (
    name varchar(30),
    abbreviation varchar(2),
    area real,
    population int,
    primary key (abbreviation)
);

---------------------------------------------------------------
--c: COVERAGE (forest no, state, percentage, area)
--     PK (forest no, state); 
--     FK (forest no) --> FOREST(forest no); 
--     FK (state) --> STATE(abbreviation); 
-- [PASTE DDL BELOW]
---------------------------------------------------------------
create table coverage (
    forest_no varchar(10),
    state varchar(2),
    percentage real,
    area real,
    foreign key (forest_no) references forest(forest_no),
    foreign key (state) references state(abbreviation)
);

---------------------------------------------------------------
--d: ROAD (road no, name, length)
--     PK (road no);
-- [PASTE DDL BELOW]
---------------------------------------------------------------
create table road (
    road_no varchar(10),
    name varchar(30),
    length real,
    primary key (road_no)
);

---------------------------------------------------------------
--e: INTERSECTION (forest no, road no)
--     PK (forest no, road no); 
--     FK (forest no) --> FOREST(forest no);
--     FK (road no) --> ROAD(road no); 
-- [PASTE DDL BELOW]
---------------------------------------------------------------
create table intersection (
    forest_no varchar(10),
    road_no varchar(10),
    primary key (forest_no, road_no),
    foreign key (forest_no) references forest(forest_no),
    foreign key (road_no) references road(road_no)
);

---------------------------------------------------------------
--f: WORKER (ssn, name, rank, employing_state)
--     PK (ssn);
--     FK (employing_state) --> STATE(abbreviation);
-- [PASTE DDL BELOW] 
---------------------------------------------------------------
create table worker (
    ssn varchar(9),
    name varchar(30),
    rank int,
    employing_state varchar(2),
    primary key (ssn),
    foreign key (employing_state) references state(abbreviation)
);

---------------------------------------------------------------
--g: SENSOR (sensor id, x, y, last charged, maintainer, last read) 
--     PK (sensor id); 
--     FK (maintainer) --> WORKER(ssn); 
-- [PASTE DDL BELOW] 
---------------------------------------------------------------
create table sensor (
    sensor_id int,
    x real,
    y real,
    last_charged timestamp,
    maintainer varchar(9),
    last_read timestamp,
    energy real,
    primary key (sensor_id),
    foreign key (maintainer) references worker(ssn)
);

---------------------------------------------------------------
--h: REPORT (sensor id, report time, temperature) 
--     PK (sensor id, report time); 
--     FK (sensor id) --> SENSOR(sensor id); 
-- [PASTE DDL BELOW] 
---------------------------------------------------------------
create table report (
    sensor_id int,
    report_time timestamp,
    temperature real,
    primary key (sensor_id, report_time),
    foreign key (sensor_id) references sensor(sensor_id)
);