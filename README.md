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

## Delete users
### Delete by email
Create a text file with one user email per line. Note an empty line will be interpreted both as an empty email and an empty string.

``` sh
python main.py --by_email users.txtzz
```

### Delete by token
Create a text file with user token per line.

``` sh
python main.py --by_token users.txt
```
### Delete by creation before date
Delete all the data of the users created before the given date relative to UTC. **Data of users created on the given date won't be deleted.** 

The date is given in partial ISO 8604 format. A simple string comparison is made. **Be careful not to forget leading '0' in dates (see last example)**

```sh
# Delete before the year 2023
python main.py --by_before_date 2023

# Delete before June 2023
python main.py --by_before_date 2023-06

# Delete before 5th of June 2023
python main.py --by_before_date 2023-06-05

# Delete before a precise moment
python main.py --by_before_date 2023-06-05T14:48:00

# CAUTION: WILL DELETE WHOLE YEAR OF 2023 (simple string comparison, '6' is bigger than '12')
python main.py --by_before_date 2023-6
```
