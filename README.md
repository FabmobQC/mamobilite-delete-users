# mamobilite-delete-users
Analyse the issue of users without email

## Installation
``` sh
pip install -r requirements.txt
```
Note it is recommanded to use a virtual environment such as venv.

## Configuration
Create a json file named config.json with one field:
- "db_url": The url of the mongodb database.


## Delete by email
Create a text file with one user email per line. Note an empty line will be interpreted both as an empty email and an empty string.

``` sh
python main.py --by_email users.txt
```

## Delete by token
Create a text file with user token per line.

``` sh
python main.py --by_token users.txt
```
