# Django-Backend

Backend project in Django for kunaisoft

## Local Development

Follow every command below to put it running in your machine

Requirements: Python

1. Setting Repository in your machine

    ```CMD
    git clone https://github.com/Rvjonh/RESTFullAPI.git     # clone the repository in the actual directory
    py -m venv .venv    # creates a python environment
    .venv\Scripts\activate.bat  # activate the environment (Windows)
    pip install -r requirements.txt     # install dependencies for the project (ej. django)
    ```

2. Configure your local variables (Windows)

    ```.ENV
    copy .env-copy .env     # Make a copy of the file
    You need to fill all the variables ... to put it work full correctly
    ```

3. Configure your database system

    In this section you will have to create a mysql database and add it to in the file django_project/settings, and modify the DATABASES section, if you have MySQL in your computer will easy, just follow these steps: [How to connect MySQL to Django](https://www.javatpoint.com/how-to-connect-mysql-to-django)

    or just change the DATABASE confi to:

    ```CMD
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    ```

4. Start the development server

    ```CMD
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
    ```

5. Visit your server website url for development (Example)

    ```CMD
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    December 25, 0000 - 07:00:00
    Django version 4.1.5, using settings 'django_project.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```

## Running Test

Already added test for user administration and CRUD in task model
Django executes test with:

```CMD
python manage.py test
```

## Generate Secrect Key

> To create a new Secreat Key for django.settings

```Python
python -c "import secrets; print(secrets.token_urlsafe())"
```
