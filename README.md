# gxforum
![screen1](.screens/screen1.png)

![screen1](.screens/screen2.png)

## About
it's a simple website that contains a forum, blog and a contact page
## Installation
Run that command to install the dependencies : (**it'is recommended to install it in a virtualenv**)

`pip install -r requirements.txt`

## Database configuration

The project uses postgresql as a database so you can switch to the default sqlite3 database by replacing DATABASES dictionary in gxforum/settings.py with :

```python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
after that you can create the database by :

```
python manage.py makemigrations
python manage.py migrate
```
## Others configurations
For simplicity purpose i did delete some password validators but it's heighly recommended to keep the default validators, for that head to the settings file "gxforum/settings.py" and change AUTH_PASSWORD_VALIDATORS into :
```python3
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

## Usage
finally you can start the developement server :
```
python manage.py runserver
```
