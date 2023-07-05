# SRE
This is the backend repository.

How to run:
First we need to run the database/db.py
  - This will create a Table in a given database if the tablename "users" doesn't exists

Then we need to run backend/app.py
  - This contains three apis:
    - register - Insert the data in the mysql database
    - login - check the credentials by checking the database if it is there it allows you to login
    - retrieve email - This helps to retrieve the email with the use of username
Additionally we encrypt and save the values in database.
while the GET call and POST call it decrypts and validates.

Containerized the repo so you can deploy with docker run commands 
