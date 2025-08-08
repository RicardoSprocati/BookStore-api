# Bookstore

Bookstore APP from Backend Python course from EBAC

## Prerequisites

```
Python 3.5>
Poetry
Docker && docker-compose

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y

```

## Quickstart

1. Clone this project

   ```shell
   git clone git@github.com:drsantos20/bookstore.git
   ```

2. Install dependencies:

   ```shell
   
   sudo apt install python3-poetry
   
   cd bookstore
   poetry install
   ```

3. Run Migrations:

   ```shell
   docker-compose exec web python manage.py migrate
   ```
   
4. Run local dev server:
   
   ```shell
   poetry run python manage.py runserver
   ```
   
5. Run docker dev server environment:

   ```shell
   docker-compose up -d --build 
   docker-compose exec web python manage.py test
   ```