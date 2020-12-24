1. install and activate virtual environments
2. export value the database credentils
example:
    export database=sammy
    export user=sammy
    export password=sammy
    export host=localhost

3. please add below table to database before run
CREATE TABLE assessment (
    id serial PRIMARY KEY,
    name varchar (255) NOT NULL,
    description text NOT NULL,
    year int,
    endyear int,
    RunTimeSec NUMERIC
);

4. start the app ***flask run --host='0.0.0.0'***

5. call the "/insert/data/add/all" api insert data from data.json