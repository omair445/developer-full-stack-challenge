

## Running the FastAPI Application

1. Create a virtual env in the root directory for the FastAPI app (Recommended)

2. Install requirements in the `src/api` directory by running; 

	`pip install -r requirements.txt`

3. Create .env file in `src/api` directory with content:
	```

	DATABASE_URL=postgresql://user:user_password@localhost/dtabase_name

	JWT_SECRET_KEY=mysecretkey

	SECRET_KEY=mysecretkey

	```
	For this project, a local postgres database was used.
	
4. Change the `sqlalchemy.url` in the `alembic.ini` file to that of the `DATABASE_URL` as seen in the code snippet below;

	 ```
	 sqlalchemy.url = postgresql://myuser:mypassword@myhost/mydatabase
	 ```

5. Run migrations with the command;

	`alembic upgrade head`

6. Run seed file in `src/api` directory with the command; 

    `python -m app.data_seeder`

7. Start the FastAPI application with the command;

	`uvicorn main:app --reload`

  

## Running the Nuxt Application

1. Go into the dashboard directory `cd src/dashboard/`

2. Install all the dependencies with the command;
	 `npm i`

3. Start the development application with 
 `npm run dev`

  
## Running the Whole App as a standalone with Docker

For this we make use of docker compose. To run the app, you can change the `DATABASE_URL` in the `docker-compose.yaml` file to your database URL like this if it needs to be updated, also change the `sqlalchemy.url` in the `alembic.ini` file to that of the `DATABASE_URL` as seen in the code snippet below;

	 ```
	 sqlalchemy.url = postgresql://myuser:mypassword@myhost/mydatabase
	 ```

``` 
environment:
	- PORT=8000
	- DATABASE_URL=postgresql://myuser:9320@localhost/mydatabase

 ```


  ## Testing
  
  Unit tests were written for both the Fastapi Application and the Nuxt Application. Integration tests and more comprehensive tests could be done but this was made simple for now
  
  ### FastAPI Application
  Pytest was used for the unit test of the Fastapi Application. To run the the tests, go into the `src/api` directory and run the command, it is recommended to use a separate test database;
  

    pytest


### Nuxt Application
  Jest was used for the unit test of the Nuxt Application. To run the the tests, go into the `src/dashboard` directory and run the command;
  

    npm test


## Overview

  

A username and password protected app that authenticates API requests using Bearer tokens (not session tokens) was created. User credentials are stored in the database and allowing to sign in using the frontend (only one user credentials was provided, as stated in the objectives). All pages, except for the login page, were made inaccessible when not signed in. 

  

### Data schema

  

The portal will be used to manage data about authors and their books. An author can have zero or more books, a book always has an author. An author just has a required name field. Books have a required name field, and a required page numbers field. Pagination, sorting and filtering were done to improve user experience and aid efficient data retrieval.

  
  

### Pages

In the portal, there are 3 pages, including the login page. A user can navigate to both pages using a nav-bar layout. Logout was also implemented

  

#### Authors

On this page, a paginated table of authors is rendered with the following columns:

- Name

- Number of books (which is calculated based on the books)

  

On top of this page, an input field that is used to search for authors is added. Next to it, a button that opens a modal to add a new author was created. When a table row was clicked on, a modal is shown to edit the author. All changes are saved to the database.

  

The modal to add/edit an author included a name field (of the author) along with a table with the books of the authors (name + number of pages). A user is able to add, edit or delete a book.

  

#### Books

On this page, a paginated table of books with the following columns is rendered :

- Name

- Author name

- Number of pages

  

On top of this page, an input field that is used to search for books is added. Next to it, a button that opens a modal to add a new book is created. When a table row is clicked on, a modal to edit the book is shown. All changes are saved to the database.

  

The modal to add/edit a book has three fields:

- Name

- Number of pages

- Author 

  
