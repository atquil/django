# django

## Setup 


### Environment Setup

```

    ## Windows
        $ cd onedrive\desktop\code
        $ mkdir drf
        $ cd drf
        $ python -m venv .venv
        $ .venv\Scripts\Activate.ps1
        (.venv) $ 
```

```
    ## macOS
        $ cd desktop/desktop/code
        $ mkdir drf
        $ cd drf
        $ python3 -m venv .venv
        $ source .venv/bin/activate
        (.venv) $
``` 

if want to do through visual studio 

```

    # macOS
        $ cd desktop/desktop/code
        $ mkdir drf
        $ cd drf
        $ code .
        $ python3 -m venv .venv
        $ source .venv/bin/activate
        (.venv) $ 
```

Sometimes you may not see it, but to double check in VS Code you can do command + Shift + p --> then check for python interpreter

### Required Installation 

Just like adding the required dependency

```
python -m pip install django
python -m pip install djangorestframework

pip install django-cors-headers 
```

Save the information about virtual environment in requirements.txt file 

```
pip freeze > requirements.txt
```

### Create Required Project now

Now with the installation, we can create the final project using `django-admin startproject <name of project> .`.

`.` will help us to create in same directory otherwise it will create a new directory for startproject. 

django-admin startproject <name of project> .
```
django-admin startproject djangoBasics . 
```

Moreover, we need to add component for this project. They are called using `startapp`. It represents, some component of the project. A project can have multiple `startapp` representing different features. 


python manage.py startapp <name of component>

```
python manage.py startapp ftpFileDownload
```

### Register the installations in Project

Go to `config` in `<nameOfProject>/settings.py` file. Add it to `INSTALLED_APPS`



```python
# djangoBasics/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Installations
    'rest_framework',
    'corsheaders',

    #Add the app here
    'ftpFileDownload',
    
]
```

Added step for CORS:
1. In `MIDDLEWARE` add `corsheaders.middleware.CorsMiddleware`

    ```python

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        #...
    ]
    ```
2. Specify which domains you want to give access to by doing the following in settings.py file

    ```
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        #...
    ]
    
    # Add configuration here
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = (
        'http://localhost:8000',
        ) 
    ```

### Initial Run for project

1. Now you can check by starting the server if everything is working fine. : 

    ```
        $   python manage.py runserver
    ```
2. Go to localhost and you will see the image: `http://127.0.0.1:8000/`
3. In terminal you can see the error :
   ```
    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    September 22, 2024 - 09:16:31
    Django version 5.1.1, using settings 'djangoBasics.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
   ```
4. Migrations are important to sync models with database even if it's not present let's do this. Also if you add any Models (Entity), we need to run migraiton to keep the project in sync
   1. `python manage.py makemigrations <appname>`
   
    ```
        $ python manage.py makemigrations ftpFileDownload 
        $ python manage.py migrate
    ```
5. Run the server again 
    ```
        $   python manage.py runserver
    ```
6. You will not find any error
   ```
   Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    September 22, 2024 - 09:23:31
    Django version 5.1.1, using settings 'djangoBasics.settings'
    Starting development server at http://127.0.0.1:8000/
   ```
###
