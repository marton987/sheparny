# Code Challenge: Python/Django Developer @ SHERPANY

Home task project to build an "events" web application.

*Author: [@marton987](https://github.com/marton987)*

## Task description

Build an "events" web application where users can log in, create 
events and sign up for an event and withdraw from an event.

Any user can list events:

- [x] Sorted so that upcoming events are first
- [x] List view shows title, date and amount of participants
- [x] List view shows the owner of the event (as the part of the email 
before the "@")
- [x] Assume there will be many thousands of events, users and participants 
per event
- [x] Any logged in user can create events
- [x] Logged in user can edit own events
- [x] Login with email and password
- [x] Registration with email and password

### Out of scope

- email confirmation
- password reset
- change password
- profile editing
- change email

## Run project

Run the next commands to run docker and start the project:

        docker-compose build
        docker-compose up
        
Then you can visit [http://localhost:3000](http://localhost:3000) to look over the events page
where you can authenticate and create new events.

Api documentation is under [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

* You can follow each README.md under [frontend/](./frontend/README.md) and [backend/](./backend/README.md) 
to start the project without Docker.

### Run project tests

Running tests

        $ docker-compose exec backend python manage.py test

Get coverage details

        $ docker-compose exec backend coverage run manage.py test
        $ docker-compose exec backend coverage report
