from __future__ import annotations  # for Python < 3.9
import json
from typing import List, Tuple, TypedDict
import getopt
import sys

from pymongo import MongoClient, database

from deletion import delete_by_email, delete_by_token, delete_by_before_date


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
    with open(file_name) as file:
        users_dirty = file.readlines()
    return [user.strip() for user in users_dirty]


def parse_options(argv: List[str]) -> Tuple[str, str]:
    def print_usage_and_leave():
        instructions = (
            "main.py --by_email <filename>"
            + "\nmain.py --by_token <filename>"
            + "\nmain.py --by_before_date <date>"
        )
        print(instructions)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(
            argv,
            "x",
            ["by_email=", "by_token=", "by_before_date="],
        )
    except getopt.GetoptError as err:
        print(err)
        print_usage_and_leave()

    total_set = 0
    mode = ""
    mode_value = ""

    for option, value in opts:
        if option == "--by_email":
            total_set += 1
        elif option == "--by_token":
            total_set += 1
        elif option == "--by_before_date":
            total_set += 1
        else:
            print_usage_and_leave()
        mode = option.replace("--", "")
        mode_value = value

    if total_set != 1:  # only one option can be set
        print_usage_and_leave()

    return mode, mode_value


def main():
    mode, mode_value = parse_options(sys.argv[1:])
    config = read_config()
    db = get_db(config["db_url"])
    if mode == "by_email":
        users_list = get_users_list(mode_value)
        delete_by_email(db, users_list)
    elif mode == "by_token":
        users_list = get_users_list(mode_value)
        delete_by_token(db, users_list)
    elif mode == "by_before_date":
        delete_by_before_date(db, mode_value)


if __name__ == "__main__":
    main()
