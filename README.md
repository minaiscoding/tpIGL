# Scientific Articles Search Engine

## Contribution guidelines

### - create a branch for each section

### - branches will follow the naming convention `<member name>/<feature or section name> `

        example: mina/authentication

### - try to provide meaningfull commit messages

        example: added an api route for user credentials

### - open a Pull Request after finishing a section or feature

## _!!! NEVER PUSH TO MAIN OR AUTOMATICALLY MERGE YOUR BRANCH TO MAIN, EVEN IF YOUR BRANCH CAN BE AUTOMATICALLY MERGED !!!_

## Description

This project is a web application designed to search scientific articles using a set of keywords

## Table of Contents

1. [Technologies](#technologies)
2. [Folder Structure](#folder-structure)
3. [Installation](#installation)

## Technologies

### Frontend:

1. ReactJS JavaScript framework
2. TailwindCSS for styling
3. GSAP (Green Socket Animation Platform) for animations

### Backend:

1. Django python library
2. SQLite relational database management system (RDBMS)


<details>
  <summary><strong>SQLite:</strong></summary>

SQLite is a self-contained, serverless, and zero-configuration relational database management system (RDBMS). It's an excellent choice for embedded systems and applications that don't require a separate database server. SQLite is the default database engine used by SQLAlchemy in this project.

[Learn more about SQLite](https://www.sqlite.org/)

</details>

## Folder Structure
## Backend

folders:
- name: server
  content:
  - name: backend
    description: Django project root
    content:
      - name: backend
        description: Django project configuration
        content:
          - name: __init__.py
          - name: asgi.py
          - name: settings.py  # Django project settings
          - name: urls.py  # Project-level URL configuration
          - name: wsgi.py
      - name: backendapp
        description: Django app for your main functionality
        content:
          - name: migrations
            content:
              - ...
          - name: __init__.py
          - name: admin.py
          - name: apps.py
          - name: models.py  # Define your Django models here
          - name: tests.py  # Write tests for your app
          - name: views.py  # Define your views here
          - ...
  
  - name: manage.py  # Django project management script
  - name: db.sqlite3  # Database with dummy data
 
- name: README.md  # Project README file


### Frontend:

- client/frontend
  - name: .gitignore (this is for not pushing the node_modules)
  - public/
    - fonts/
    - images/
  - src/
    - components/ (folders of React components, each page has a separate folder)
    - pages/ (all the pages of the website)
    - styles/ (contains global styling where raw CSS is required, use TailwindCSS otherwise)
  - App.js (this is where all pages will be called and where routes are handled)

## Installation

### Frontend

- If you don't have Node.js installed, navigate to (https://nodejs.org/en) and download the latest stable version (LTS) then install it.

- Navigate to the frontend folder
  `cd client/frontend`
- Run the command
  `npm install`
- Start the development server by running
  ` npm start`
- CTRL + Click the link displayed in the terminal to view the local development server.

### Backend

- If you don't have Python installed, navigate to (https://www.python.org/downloads/) and download the last release then install it.
- Navigate to the backend folder
  `cd server/backend`
# Elasticsearch Setup:

- Download and install Elasticsearch from elastic.co.
- go to elasticsearch/config/elascticsearch.yml and change xpath.security.enable to false
- Start Elasticsearch service by clicking on bin/elasticsearch.bat in the elastic search folder
- Install Django by typing the command
  `pip install Django`
- install elascticsearch lib by typing the command
  `pip install elasticsearch-dsl elasticsearch`
- Start the django server by running
  `python manage.py runserver`

#### Starting the database

- Open a terminal and make sure you are at the backend folder
- Start a python shell by typing
  `python`
- Inside the python shell, enter the following 2 commands
  ```python
  from app import app, db
  ```
  ```python
  with app.app_context():
    db.create_all()
  ```
  this will create an SQLite database file with the specified name in config.py containing all the database tables defined in models
