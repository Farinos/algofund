donation-contract

# Algofund API

## Setup

Clone sandbox node repository:
`git clone https://github.com/algorand/sandbox.git`
Switch directory:
`cd sandbox`
Execute sandbox containers with private network with following command:
`./sandbox up`

## Usage

- create your venv named **algofund-venv** `python -m venv algofund-venv`
- activate your venv with `source algofund-venv/bin/activate`
- install all the project dependencies with `pip install -r requirements.txt`
- go to algofund directory `cd algofund`
- run the server `python manage.py runserver`

Admin info:
```
Admin portal at /admin
username: admin
password: admin
email: admin@api.com
```

# Smart Contract

Per creare il portafogli bisogna inserire 25 parole per poi andare a creare la private key

- withdraw si fa innescando una noop mandando come parametro una "withdraw"
- creazione contratto maandare 0
- `applicationIndex` è id dello smart contract e serve per sapere id del contratto su cui andare a deployare i dati, anche per fare il widthraw ecc
- `fundPool` è una transazione esterna al contratto che prende le info del sender, retrieve del address del receiver ed invia i dati

# Python venv

- to create a Python venv use the command `python -m venv <name-of-venv>` where `-m` indicates to Python to execute *venv* module as a script
- to activate a *venv* you need to use the `source <name-of-venv>/bin/activate` command
- to deactivate a *venv* use `deactivate` command

## Pip with environments

- after you activated the *venv* you can install all the dependencies with `pip install -r requirements.txt`
- **requirements.txt** is the file containing all the project dependencies, you can generate the file by running the command `pip freeze > requirements.txt`

# Django

[Guide](https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c)

- start Django project `django-admin startproject algofund`
- run the project `python manage.py runserver`
- create a new app for our API `python manage.py startapp api`
- register the new app inside the main project *algofund/setting.py*
```python
INSTALLED_APPS = [
    'api.apps.ApiConfig',
    ...
]
```
- migrate already existing databases `python manage.py migrate`
- create **superuser** with `python manage.py createsuperuser`
- whenever we make changes or define a new model we need to tell Django to migrate those changes `python manage.py makemigrations && python manage.py migrate`
- remember to register models you want to manage with **admin account** inside *admin.py* file

# Django REST framework

Now we want to serialize data from our database via endpoints:
- install Django REST framework `pip install djangorestframework`
- tell Django the REST framework inside `mysite/settings.py` has been installed
```python
INSTALLED_APPS = [
    'rest_framework',
    ...
]
```
- create `serializers.py` inside `api` folder, here we need to create the serializer
- create a serializer class inside `api/views.py` file
- `router` imported from `rest_framework` is responsible of dinamically routing requests to the right resource in a dinamic way, so if we add or delete items from the db the URLs will update to match. A router works with a `viewset` to dinamically route requests.  

# TODO

- invoke algo functions on post fund, pool and get funds
- fix image retrieval broken link