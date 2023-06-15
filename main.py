from __future__ import annotations
import json
from typing import TypedDict
from typing import List
import getopt
import sys

from pymongo import MongoClient, database

from deletion import delete_by_email, delete_by_token


class Config(TypedDict):
    db_url: str


def read_config() -> Config:
    with open("config.json") as config_file:
        config = json.load(config_file)

    return dict(
        db_url=config["db_url"],
    )


def get_db(db_url: str) -> database.Database:
    client: MongoClient = MongoClient(db_url)
    return client.Stage_database


def get_users_list(file_name: str) -> List[str]:
    with open(file_name) as user_file:
        users = user_file.readlines()
    return users


def parse_options(argv: List[str]):
    def print_usage_and_leave():
        instructions = "main.py --by_email <file>" + "\nmain.py --by_token <file>"
        print(instructions)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(
            argv,
            "x",
            [
                "by_email=",
                "by_token=",
            ],
        )
    except getopt.GetoptError as err:
        print(err)
        print_usage_and_leave()

    by_email = False
    by_token = False
    file_name = None

    for option, value in opts:
        file_name = value
        if option == "--by_email":
            by_email = True
        elif option == "--by_token":
            by_token = True
        else:
            print_usage_and_leave()

    if by_email == by_token:  # both false or both true
        print_usage_and_leave()

    return by_email, file_name


def main():
    is_by_email, file_name = parse_options(sys.argv[1:])
    config = read_config()
    db = get_db(config["db_url"])
    users_list = get_users_list(file_name)
    if is_by_email:
        delete_by_email(db, users_list)
    else:
        delete_by_token(db, users_list)


if __name__ == "__main__":
    main()
