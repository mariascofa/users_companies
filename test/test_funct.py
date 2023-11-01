import json
import os
from unittest import TestCase

from src.funct_example import (
    load_json,
    check_age_condition,
    add_fullname_to_users,
    filter_users_by_age,
    associate_users_with_companies,
    users_companies_comprehension,
    company_connection_non_mod,
    save_data_to_json,
)


class TestFunctions(TestCase):
    def test_load_json(self):
        exp_result = [
            {
                "id": 1,
                "name": "Head Journal",
                "headquarters": "San Francisco",
                "industry": "Tech",
            },
            {
                "id": 2,
                "name": "Au Revoir Health",
                "headquarters": "Paris",
                "industry": "Health",
            },
            {
                "id": 3,
                "name": "Solomon Sisters Bank",
                "headquarters": "London",
                "industry": "Finance",
            },
        ]
        app_res = load_json("test/data/company.json")
        self.assertEqual(exp_result, app_res)

    def test_check_age_condition_false(self):
        result = check_age_condition(
            condition="Less than", result_age=35, condition_age=20
        )
        self.assertEqual(result, False)

    def test_check_age_condition_true(self):
        result = check_age_condition(
            condition="Greater than or equal to", result_age=12, condition_age=12
        )
        self.assertEqual(result, True)

    def test_add_fullname_to_users(self):
        inputs = [
            {
                "forename": "Jane",
                "surname": "Smith",
                "date_of_birth": "2001/10/12",
                "location": "London",
                "company_id": 3,
            }
        ]
        outputs = [
            {
                "forename": "Jane",
                "surname": "Smith",
                "full_name": "Jane Smith",
                "date_of_birth": "2001/10/12",
                "location": "London",
                "company_id": 3,
            }
        ]
        result = add_fullname_to_users(user_data_set=inputs)

        for item_index in range(len(outputs)):
            for key, value in outputs[item_index].items():
                self.assertEqual(result[item_index][key], value)

    def test_filter_users_by_age(self):
        inputs = [
            {
                "forename": "Jane",
                "surname": "Smith",
                "date_of_birth": "2022/10/12",
                "location": "London",
            },
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company_id": 3,
            },
        ]
        outputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company_id": 3,
            }
        ]
        result = filter_users_by_age(
            data_set=inputs, selected_age=15, condition="Greater than"
        )

        self.assertEqual(result, outputs)

    def test_associate_users_with_companies(self):
        inputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company_id": 3,
            }
        ]
        outputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company": {
                    "id": 3,
                    "name": "Solomon Sisters Bank",
                    "headquarters": "London",
                    "industry": "Finance",
                },
            },
        ]
        with open("test/data/company.json", "r") as file:
            json_string = file.read()
            company_data = json.loads(json_string)

        result = associate_users_with_companies(
            user_data_set=inputs, company_data_set=company_data
        )

        self.assertEqual(result, outputs)

    def test_users_companies_comprehension(self):
        inputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company_id": 3,
            }
        ]
        outputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company": {
                    "id": 3,
                    "name": "Solomon Sisters Bank",
                    "headquarters": "London",
                    "industry": "Finance",
                },
            },
        ]
        with open("test/data/company.json", "r") as file:
            json_string = file.read()
            company_data = json.loads(json_string)

        result = users_companies_comprehension(
            user_data_set=inputs, company_data_set=company_data
        )

        self.assertEqual(result, outputs)

    def test_company_connection_non_mod(self):
        inputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company_id": 3,
            }
        ]
        outputs = [
            {
                "forename": "Bob",
                "surname": "Smith",
                "date_of_birth": "2000/12/30",
                "location": "London",
                "company": {
                    "id": 3,
                    "name": "Solomon Sisters Bank",
                    "headquarters": "London",
                    "industry": "Finance",
                },
            },
        ]
        with open("test/data/company.json", "r") as file:
            json_string = file.read()
            company_data = json.loads(json_string)

        result = company_connection_non_mod(
            user_data_set=inputs, company_data_set=company_data
        )

        self.assertEqual(result, outputs)

    def test_save_data_to_json(self):
        data_to_save = [
            {
                "id": 1,
                "name": "Head Journal",
                "headquarters": "San Francisco",
                "industry": "Tech",
            },
            {
                "id": 2,
                "name": "Au Revoir Health",
                "headquarters": "Paris",
                "industry": "Health",
            },
            {
                "id": 3,
                "name": "Solomon Sisters Bank",
                "headquarters": "London",
                "industry": "Finance",
            },
        ]
        json_path = "test/data/temp_test_file.json"
        try:
            save_data_to_json(json_path, data_to_save)
            self.assertTrue(os.path.exists(json_path))
            with open(json_path, "r") as json_file:
                saved_data = json.load(json_file)

            self.assertEqual(saved_data, data_to_save)

        finally:
            if os.path.exists(json_path):
                os.remove(json_path)
