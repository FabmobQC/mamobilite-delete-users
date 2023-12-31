from __future__ import annotations  # for Python < 3.9
from typing import List

from pymongo import database


def delete_user(db: database.Database, users_list: List[str]):
    print(f"Deleting users: {users_list}")
    db.Stage_analysis_timeseries.delete_many({"user_id": {"$in": users_list}})
    db.Stage_pipeline_state.delete_many({"user_id": {"$in": users_list}})
    db.Stage_timeseries.delete_many({"user_id": {"$in": users_list}})
    db.Stage_usercache.delete_many({"user_id": {"$in": users_list}})
    # Last to make it possible to retrieve the user_id in case of failure
    db.Stage_uuids.delete_many({"uuid": {"$in": users_list}})
    # Really last to make it possibleto retrieve the user_id in case of failure
    db.Stage_Profiles.delete_many({"user_id": {"$in": users_list}})


def get_user_ids_by_email(db: database.Database, email: str | None) -> List[str]:
    cursor = db.Stage_Profiles.find({"email": email})
    return [user["user_id"] for user in cursor]


def get_user_ids_by_token(db: database.Database, token: str) -> List[str]:
    cursor = db.Stage_uuids.find({"user_email": token})
    return [user["uuid"] for user in cursor]


def get_user_ids_by_before_date(db: database.Database, date: str) -> List[str]:
    cursor = db.Stage_Profiles.find({"creation_ts": {"$lt": date}})
    user_ids = [user["user_id"] for user in cursor]
    return user_ids


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


def delete_by_before_date(db: database.Database, date: str):
    user_ids = get_user_ids_by_before_date(db, date)
    delete_user(db, user_ids)
