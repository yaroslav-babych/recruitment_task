# Recruitment Task

## Description

This is a Django application that allows you to create dynamic models based on user input. The user is able to define a model name and its fields through an API. Once the model is defined, the user can make GET, POST requests to the API to manipulate the data in the defined model.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone this repository.
2. Navigate to the project directory.
3. Run `docker-compose up --build` to build the images and start the containers.
4. Run `docker-compose exec web python manage.py migrate`
5. Navigate to http://localhost:8000/api/ to access the API endpoints.

## API Endpoints

The following endpoints are available for this application:

| Endpoint                             | HTTP Method | Result                                           |
|--------------------------------------|-------------|--------------------------------------------------|
| api/table/                           | GET         | Retrieve all tables (schemas) in the database     |
| api/table/                           | POST        | Create a new table (schema) in the database       |
| api/table/{id}/                      | GET         | Retrieve a specific table (schema) in the database|
| api/table/{id}/                      | PUT         | Update a specific table (schema) in the database  |
| api/table/{id}/add_row/              | POST        | Add a new row to a specific table (schema)         |
| api/table/{id}/get_rows/             | GET         | Retrieve all rows of a specific table (schema)     |

## Running Tests

To run the test suite, run the following command from the project directory:

```bash
docker-compose exec web python manage.py test
```

>Please note that there is no logic for tests to use SQLite, and I do not recommend running tests in the same database as the live environment. It is advised to use a separate database for testing purposes.

> Warning: It is strongly recommended to not run tests in the same database where live run is, as it can cause data loss and other issues. Please use a separate database for testing purposes.