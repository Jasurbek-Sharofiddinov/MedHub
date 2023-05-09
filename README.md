## MedHub - A Patient Management System

### Steps to run the project
1. Clone the repository
2. Create '.env' file in the root directory and add the following variables
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_HOST
POSTGRES_PORT
```
3. Run the following commands
```
docker-compose build
docker-compose up
```
4. Open the browser and go to http://localhost:8000/
5. To access the admin panel, go to http://localhost:8000/admin
6. To access the API root, go to http://localhost:8000/api
7. To access the Swagger API documentation, go to http://localhost:8000/swagger
8. To access the Redoc API documentation, go to http://localhost:8000/redoc
9. To access the API documentation, go to http://localhost:8000/docs


### Steps to run tests
1. Run the following commands after the project is running
```
docker-compose run --rm app pytest -vvv
```
