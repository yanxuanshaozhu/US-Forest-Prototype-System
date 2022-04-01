<h1>US Forest System</h1>

## Description

---

This is a database management course project. It's a web application that allows users to conduct CURD on a database that mimics the forests in the United States.

## Project Structure

---

Front end: a web application built on Plotly Dash, deployed to Heroku; Bootstrap<br>
Back end: web servers built on Spring Boot, deployed to Heroku<br>
Database: PostgreSQL, based on Heroku Postgres

## Run this project on Heroku(recommended)

---

<p style="color:red;font-weight:bold;"> This project has been deployed to heroku, click this <a href="https://dbprojectfrontend.herokuapp.com/">link</a> to have a try (it takes for a while for the frontend to load).</p>

## Run this project on your local machine

---

### Database settings

1. Run the `create_table.sql` in your local PostgreSQL 

### Backend settings

1. Open `dbprojectbackend` directory  in IntelliJ IDEA, modify the `application.properties` file:

```properties
# The following line should be your local PostgreSQL url string
spring.datasource.url=  
# The following line should be your PostgreSQL username
spring.datasource.username= 
# The following line should be your PostgreSQL password
spring.datasource.password= 
spring.datasource.driver-class-name=org.postgresql.Driver

```

2. Run the `main` method in `DemoApplication.java` file, then the server should be running at `http://127.0.0.1:8080/`

### Frontend settings

1. Open `dbprojectfrontend` directory  in PyCharm, install all packages in the `requirements.txt` file using `pip install <package name>`  (You should install Python first to use pip)

2. Change all URLs in `request.get()` and `request.post()` method. For example. if the URL is `https://dbprojectbackend.herokuapp.com/forest/display`, you should change it to `localhost:8080/forest/display` or `http://127.0.0.1:8080/forest/display`

3. You may need to add the following settings if you cannot request localhost using requests in Python

   ```python
   import os
   os.environ['NO_PROXY'] = '127.0.0.1'
   ```


4.  Run the `index.py` file, then the frontend should be running at `http://127.0.0.1:8050/` 

## Project logistics

---

### <span style="color:red;">State table </span> 

I allow the user to update a state table:  if the users encounter problems that state name or state abbreviation does not exist, she can insert states into the state table.

`name`: if the state name is in the state table, cannot add state

`abbreviation`: if the state abbreviation is in the state table, cannot add state, the length should be 2

`area`: state area should be a positive real number

`population`: state population should be a positive integer

### Task 1: add forest

`forest_no`: sum of rows in forest table plus one

`name`: if the forest name is in the database, cannot add forest

`area`, `acid_level`, `mbr_xmin`, `mbr_xmax`, `mbr_ymin`, `mbr_ymax`: should be positive real numbers

`state`: the state name should be in the state table

### Task 2: add worker

`ssn`: the length of SSN should be 9, if the worker SSN is in the database, cannot add worker

`name`: if the worker name is in the database, cannot add worker

`rank`: should be a positive integer

`abbreviation`: the state abbreviation should be in the state table, the length of state abbreviation should be 2

### Task 3: add sensor

`sensor_id`: should be a positive integer, if the sensor_id is in the database, cannot add sensor

`x`, `y`: the x and y coordinates should be non-negative real numbers, if the sensor coordinates is in the database, cannot add sensor

`maintainer`: this can be empty, we allow a sensor without a maintainer to be added; if the maintainer SSN is not empty, then its length should be 9

`last_charged`, `last_read`: should be timestamp without timezone

`energy`: sensor energy should be a non-negative real number

### Task 4: switch worker duties

`name1`: the name of worker1 should in the worker table

`name2`: the name of worker2 should be in the worker table, the name of worker2 should not be the same as the name of worker1, the two workers should work in the same state

### Task 5: update sensor status

`x`, `y`: the x and y coordinates should be non-negative real numbers, if there is not sensor at the location specified by the two coordinates, cannot update sensor status

`energy`: sensor energy should be a non-negative real number

`temperature`: the temperature should be a real number(temperature can be negative)

`last_charged`: should be timestamp without timezone

`last_read`: after update, the sensor last_read should be current time (now)

### Task6：update forest covered area

`name`: forest name should be in the forest table, otherwise cannot update coverage

`area`: should be a positive real number

`abbreviation`: state abbreviation should be in the state table, its length should be 2

### Task 7: find top k busy workers

`k`: should be a positive integer

### Task 8: display sensor ranking

`k`: in order to display the most active <span style="color:red;font-weight:bold;"> sensors</span>  as instructed in the pdf, should allow user to input a positive integer k to display top k active sensors

### Task 9: Transaction and concurrency control

1. The `JdbcTemplate` in Spring Boot  uses `PreparedStatement`, so there is not chance for SQL injection
2. The `@EnableTransactionManagement` and `@Transactional` annotations in Spring Boot ensures SQL transactions and currency control work properly

## Limitations and to be done

---

### Limitations

Since I'm new to the Spring Boot framework and Dash web framework, there are lots of staff that could be improved

### To be done

- [ ] Refactor the backend project according to the MVC model
- [ ] Improve frontend UI



