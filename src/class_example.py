import json
import warnings
from datetime import date, datetime

from src.data.models import Condition


class DataProcessor:
    def __init__(
        self,
        users_json_path: str,
        company_json_path: str,
    ):
        """
        Initialize the DataProcessor with the paths to user and company JSON files.

        :param users_json_path: Path to the user JSON file.
        :param company_json_path: Path to the company JSON file.
        """
        self.users_json_path = users_json_path
        self.company_json_path = company_json_path

    def load_json(self, json_path: str):
        with open(json_path, "r") as file:
            json_string = file.read()
        return json.loads(json_string)

    def _check_age_condition(
        self, condition: str, result_age: int, condition_age: int
    ) -> bool:
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

    def add_fullname_to_users(self) -> list:
        """
        Add a "full_name" field to each user in the data set based on the "forename" and "surname" fields.

        :return: The updated user data set with "full_name" field.
        """
        data_set = self.load_json(self.users_json_path)
        return [
            {**user, "full_name": f"{user['forename']} {user['forename']}"}
            for user in data_set
        ]

    def filter_users_by_age(self, selected_age: int, condition: str) -> list:
        """
        Filter users in the data set based on age and a specified condition.

        :param selected_age: The age to compare with. Selected by the user.
        :param condition: The condition for comparison (e.g., "Less than"). Selected by the user.
        :return: List of filtered users.
        """
        data_set = self.load_json(self.users_json_path)
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
                if self._check_age_condition(
                    condition=condition, result_age=age, condition_age=selected_age
                ):
                    updated_set.append(user)
        return updated_set

    def associate_users_with_companies(self) -> list:
        """
        Associate users with their respective companies and remove "company_id" from user data.

        :return: The updated user data set with associated companies.
        """
        user_data_set = self.load_json(self.users_json_path)
        company_data_set = self.load_json(self.company_json_path)

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

    def users_companies_comprehension(self) -> list:
        """
        Associate users with their respective companies and remove "company_id" from user data using list comprehension.

        :return: The updated user data set with associated companies.
        """
        user_data_set = self.load_json(self.users_json_path)
        company_data_set = self.load_json(self.company_json_path)

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

    def company_connection_non_mod(self) -> list:
        """
        Associate users with their respective companies and remove "company_id" from user data using list comprehension.

        :return: A list of user data dictionaries with associated companies.

        """
        user_data_set = self.load_json(self.users_json_path)  # Use users_json_path here
        company_data_set = self.load_json(
            self.company_json_path
        )  # Use company_json_path here

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

    def save_data_to_json(self, json_file_path, data):
        """
        Save a Python data structure as JSON to a specified file.

        :param json_file_path: The path to the JSON file where the data will be saved.
        :param data: The Python data structure (e.g., list, dictionary) to be saved as JSON.
        """
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file)


processor = DataProcessor(
    users_json_path="/home/mariya/users_companies/assets/user.json",
    company_json_path="/home/mariya/users_companies/assets/company.json",
)


user_data = processor.load_json(processor.users_json_path)
users_with_fullname = processor.add_fullname_to_users()

selected_age = 30
condition = "Less than"
filtered_users = processor.filter_users_by_age(selected_age, condition)

users_with_companies = processor.associate_users_with_companies()

output_data = users_with_companies
output_json_file_path = "output_data.json"
processor.save_data_to_json(output_json_file_path, output_data)
