donation-contract

# Algofund API

## Setup

Clone sandbox node repository:
`git clone https://github.com/algorand/sandbox.git`
Switch directory:
`cd sandbox`
Execute sandbox containers with private network with following command:
`./sandbox up dev`

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

# FINAL PRESENTATION

- struttura del progetto
- webapp e tutto in localhost
- README.md
- 1 smart contract per ogni pool

# TEST

GET list of pools `http://localhost:8000/pools/`, example of response:
```json
[
    {
        "id": 5,
        "name": "4",
        "description": "this is the 4th test",
        "applicationIndex": "dsd1237493875493274983279",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/newrelic.png"
    },
    {
        "id": 6,
        "name": "6",
        "description": "6",
        "applicationIndex": "6",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/firma.png"
    },
    {
        "id": 8,
        "name": "989",
        "description": "89989",
        "applicationIndex": "98978766",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/Screenshot_from_2021-11-10_17-58-40.png"
    },
    {
        "id": 7,
        "name": "ezara",
        "description": "ezara",
        "applicationIndex": "123456576",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/ezara.jpeg"
    },
    {
        "id": 9,
        "name": "fewfewfewfewf",
        "description": "fedwsfwfew",
        "applicationIndex": "23232543453453453452",
        "minAmount": 300,
        "expiryTime": "2022-06-23",
        "image": null
    },
    {
        "id": 2,
        "name": "test",
        "description": "The very first pool test",
        "applicationIndex": "123456789",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/ezara.jpeg"
    },
    {
        "id": 10,
        "name": "test16",
        "description": "faaaaa",
        "applicationIndex": "2",
        "minAmount": 200,
        "expiryTime": "2022-06-23",
        "image": null
    },
    {
        "id": 3,
        "name": "test2",
        "description": "the second test",
        "applicationIndex": "987654321",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/ezara.jpeg"
    },
    {
        "id": 11,
        "name": "testdatetime",
        "description": "Test datetime",
        "applicationIndex": "3",
        "minAmount": 300,
        "expiryTime": "2022-07-24",
        "image": null
    },
    {
        "id": 4,
        "name": "third test",
        "description": "this is the third test",
        "applicationIndex": "1237493875493274983279",
        "minAmount": 100,
        "expiryTime": "2022-06-11",
        "image": "http://127.0.0.1:8000/media/pictures/cic.png"
    }
]
```

GET data of a single pool by primary key (id) `http://localhost:8000/pools/<id>`:
```json
{
    "id": 11,
    "name": "testdatetime",
    "description": "Test datetime",
    "applicationIndex": "3",
    "minAmount": 300,
    "expiryTime": "2022-07-24",
    "image": "http://127.0.0.1:8000/media/pictures/cic.png"
}
```

POST pool `http://localhost:8000/pools/` with body:
```json
{
    "name": "test11",
    "description": "fedwsfwfew",
    "applicationIndex": "23232543453453453452",
    "minAmount": 300,
    "expiryTime": "2022-06-23",
    "creatorMnemonic": "fine april congress twelve cave welcome slogan salt nice domain camp excuse door wool secret toss tell brush chicken chief swear sorry awkward above deposit",
    "image": "base64encoded image"
}
```

POST fund on pool `http://localhost:8000/pools/<id>/funds` with body:
```json
{
    "senderMnemonic": "oblige later shift bless able draw journey behave offer fox easily pottery maid vehicle grow math promote infant admit reopen good pulp survey able into",
    "amount": "100000"
}
```

Address -> mnemonic
```
JKOAFKX5DHKBSV5CTNIAM26G2EQT5MHQGZT6NVXTW7WQTDNXMIMDJF2Z4U -> "fine april congress twelve cave welcome slogan salt nice domain camp excuse door wool secret toss tell brush chicken chief swear sorry awkward above deposit"

WRLWIIZDSWJDR47JOPCICHBLF23OHBMJUHAH7PZLSHPZX4P673XQ76G3YA -> "oblige later shift bless able draw journey behave offer fox easily pottery maid vehicle grow math promote infant admit reopen good pulp survey able into"
```

# Algorand commands

```shell
./sandbox up dev # start Algorand containers with dev data
./sandbox goal account list
./sandbox goal account balance -a <wallet-address> # show balance of person/contract
./sandbox goal app read --app-id <smartContractApplicationIndex> -d data  
./sandbox goal account export -a <wallet-address> # export mnemonic
```