import json
import warnings
from datetime import date, datetime

from src.data.models import Condition


def load_json(json_path: str):
    """
    Load JSON data from a file and return it as a Python dictionary.

    :param json_path: Path to the JSON file.
    :return: Loaded JSON data as a Python dictionary.
    """
    with open(json_path, "r") as file:
        json_string = file.read()
    return json.loads(json_string)


def check_age_condition(condition: str, result_age: int, condition_age: int) -> bool:
    """
    Check if a condition is met based on the result age and condition age.

    :param condition: The condition to check (e.g., "Less than").
    :param result_age: The result age for comparison.
    :param condition_age: The age to compare with. Selected by the user.
    :return: True if the condition is met, False otherwise.
    """
    comparison_operations = {
        Condition.LESS_THAN: result_age < condition_age,
        Condition.GREATER_THAN: result_age > condition_age,
        Condition.LESS_OR_EQUAL: result_age <= condition_age,
        Condition.GREATER_OR_EQUAL: result_age >= condition_age,
        Condition.EQUAL: result_age == condition_age,
        Condition.NOT_EQUAL: result_age != condition_age,
    }
    return comparison_operations.get(condition, False)


# Task 1
def add_fullname_to_users(user_data_set: list) -> list:
    """
    Add a "full_name" field to each user in the data set based on the "forename" and "surname" fields.

    :param user_data_set: The user data set to update.
    :return: The updated user data set with "full_name" field.
    """
    return [
        {**user, "full_name": f"{user['forename']} {user['forename']}"}
        for user in user_data_set
    ]


# Task 2 EXPANDED
def filter_users_by_age(data_set: list, selected_age: int, condition: str) -> list:
    """
    Filter users in the data set based on age and a specified condition.

    :param data_set: The data set to filter.
    :param selected_age: The age to compare with. Selected by the user.
    :param condition: The condition for comparison (e.g., "Less than"). Selected by the user.
    :return: List of filtered users.
    """
    updated_set = []
    for user in data_set:
        date_of_birth = user["date_of_birth"]
        try:
            parsed_date = datetime.strptime(date_of_birth, "%Y/%m/%d")
        except ValueError:
            warnings.warn(
                f"User {user['forename']} {user['surname']} has incorrect date of birth format."
            )
        else:
            today = date.today()
            age = (
                today.year
                - parsed_date.year
                - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
            )
            if check_age_condition(
                condition=condition, result_age=age, condition_age=selected_age
            ):
                updated_set.append(user)
    return updated_set


# Task 3.1
def associate_users_with_companies(user_data_set: list, company_data_set: list) -> list:
    """
    Associate users with their respective companies and remove "company_id" from user data.

    :param user_data_set: The user data set.
    :param company_data_set: The company data set.
    :return: The updated user data set with associated companies.
    """
    existing_company_ids = {company["id"]: company for company in company_data_set}
    for user in user_data_set:
        company_id = user["company_id"]
        if company_id in existing_company_ids:
            company_data = existing_company_ids[user.pop("company_id")]
            user["company"] = company_data
        else:
            warnings.warn(
                f"User {user['forename']} {user['surname']} has unrecognized company id: {user['company_id']}."
            )
    return user_data_set


# Task 3.2
def users_companies_comprehension(user_data_set: list, company_data_set: list) -> list:
    """
    Associate users with their respective companies and remove "company_id" from user data using list comprehension.

    :param user_data_set: The user data set.
    :param company_data_set: The company data set.
    :return: The updated user data set with associated companies.
    """
    existing_company_ids = {company["id"]: company for company in company_data_set}
    updated_set = [
        {**user, "company": existing_company_ids[user["company_id"]]}
        for user in user_data_set
        if user["company_id"] in existing_company_ids
    ]
    for user in updated_set:
        user.pop("company_id", None)
    for user in user_data_set:
        if user["company_id"] not in existing_company_ids:
            warnings.warn(
                f"User {user['forename']} {user['surname']} has unrecognized company id: {user['company_id']}."
            )
    return updated_set


# Task 3.3 WITHOUT POP METHOD
def company_connection_non_mod(user_data_set: list, company_data_set: list) -> list:
    """
    Associate users with their respective companies and remove "company_id" from user data using list comprehension.

    :param user_data_set: A list of user data dictionaries.
    :param company_data_set: A list of company data dictionaries.
    :return: A list of user data dictionaries with associated companies.
    """
    existing_company_ids = {company["id"]: company for company in company_data_set}
    updated_set = []

    for user in user_data_set:
        company_id = user["company_id"]

        if company_id in existing_company_ids:
            updated_dict = {
                key: value for key, value in user.items() if key != "company_id"
            }
            updated_dict["company"] = existing_company_ids[company_id]
            updated_set.append(updated_dict)
        else:
            warnings.warn(
                f"User {user['forename']} {user['surname']} has an unrecognized company id: {user['company_id']}."
            )

    return updated_set


def save_data_to_json(json_file_path, data):
    """
    Save a Python data structure as JSON to a specified file.

    :param json_file_path: The path to the JSON file where the data will be saved.
    :param data: The Python data structure (e.g., list, dictionary) to be saved as JSON.
    """
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file)
