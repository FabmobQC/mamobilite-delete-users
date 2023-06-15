from __future__ import annotations  # for Python < 3.9
from typing import List

from pymongo import database


def delete_user(db: database.Database, users_list: List[str]):
    print(f"Deleting users: {users_list}")


def get_user_ids_by_email(db: database.Database, email: str | None) -> List[str]:
    cursor = db.Stage_Profiles.find({"email": email})
    return [user["user_id"] for user in cursor]


def get_user_ids_by_token(db: database.Database, token: str) -> List[str]:
    cursor = db.Stage_uuids.find({"user_email": token})
    return [user["uuid"] for user in cursor]


def delete_by_token(db: database.Database, users_list: List[str]):
    for user_token in users_list:
        user_ids = get_user_ids_by_token(db, user_token)
        delete_user(db, user_ids)


def delete_by_email(db: database.Database, users_list: List[str]):
    for user_email in users_list:
        if user_email == "":  # Delete users with empty email
            user_ids = [
                *get_user_ids_by_email(db, ""),
                *get_user_ids_by_email(db, None),
            ]
        else:
            user_ids = get_user_ids_by_email(db, user_email)
        delete_user(db, user_ids)
