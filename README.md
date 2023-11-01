#### This assessment has been solved in two approaches:
- Through the class - `src/class_example.py`
- As separate functions - `src/funct_example.py`

Separate functions have been tested in `test/test_funct.py`.

### Task 1

Transform the user collection so each record contains a new `full_name` field as shown in the example below.

```js
{
    "forename": "Jane",
    "surname": "Smith",
    "full_name": "Jane Smith",
    "date_of_birth": "2001/10/12",
    "location": "London",
    "company_id": 3
}
```

#### Solution:
- In `src/funct_example.py` task is solved through the `add_fullname_to_users` function.
- In `src/class_example.py` task is solved through the method `add_fullname_to_users`, which provides a structured approach to working with user data.
The method first loads the user data from the specified JSON file using the `load_json` function.

#### Usage Example:

The usage of the `DataProcessor` class to perform this transformation is demonstrated in the provided code. The transformed user data, which now includes the `full_name` field, can be further processed or saved to an output JSON file.

```python
processor = DataProcessor(
    users_json_path="assets/user.json",
    company_json_path="ssets/company.json",
)

# Transform user data by adding full names
users_with_fullname = processor.add_fullname_to_users()

```

### Task 2

Transform the user collection, so it only contains records where the user is 30 years in age or older.

#### Solution:
In `src/funct_example.py` task is solved through the `filter_users_by_age` function. 
I've expanded features of this task, so now user will be able to select age group, that they want,
by choosing comparing condition (from a drop-down in the inputs field), such as "Less than," "Greater than," etc. 
and the desired age to compare with. So they can select users who are younger than, for example, 20 years or older.

It takes the following parameters:

- `data_set`: The data set to be filtered.
- `selected_value`: Age that will be compared to.
- `condition`: The condition for comparison (e.g., "Less than," "Greater than," etc.).

The function iterates through the data set and checks each record against the specified condition and selected value. If the condition is met, the record is included in the filtered result.

#### Date Parsing and Error Handling

The code attempts to parse date values in the data set. If a date is not in the expected format (YYYY/MM/DD), a warning message is generated to alert the user. This ensures that data inconsistencies are handled gracefully.

#### Conditions Handling

A custom `Condition` enum is used to handle various conditions, such as "Less than," "Greater than," "Less than or equal to," "Greater than or equal to," "Is equal to," and "Is not equal to." These conditions provide flexibility for users to define their filtering criteria.

In `src/class_example.py` task is solved through the method `filter_users_by_age`.

#### Usage Example:
```python
# Initialize the DataProcessor with file paths
processor = DataProcessor(
    users_json_path="assets/user.json",
    company_json_path="assets/company.json",
)

selected_age = 30
condition = "Less than"

filtered_users = processor.filter_users_by_age(selected_age, condition)

# You can save the filtered data to a JSON file using the save_data_to_json function. 
# In this example, we save the filtered user data to the "output_data.json" file.

output_json_file_path = "output_data.json"
processor.save_data_to_json(output_json_file_path, filtered_users)
```

### Task 3

Transform the user collection so each record contains a new `company` field which contains the company object 
and replaces the `company_id` field as shown in the example below.

This should be based on the relationship defined by the `company_id` field contained in the user collection 
and the `id` field contained in the company collection.


js
{
    "forename": "Jane",
    "surname": "Smith",
    "date_of_birth": "2001/10/12",
    "location": "London",
    "company": {
        "id": 3,
        "name": "Solomon Sisters Bank",
        "headquarters": "London",
        "industry": "Finance"
    }
}

#### Solution:
In `src/funct_example.py` task is solved through different approaches:
- function `associate_users_with_companies` is using mutation method 'dict.pop()', that removes 'company_id' key, after it was used.
- function `users_companies_comprehension` is using list comprehension and mutation method 'dict.pop()', that removes 'company_id' key, after it was used.
- function `company_connection_non_mod` is not using doing any mutation methods.


In `src/class_example.py` task is solved through the method `associate_users_with_companies`.

#### Usage Example:
```python
# Initialize the DataProcessor with file paths
processor = DataProcessor(
    users_json_path="assets/user.json",
    company_json_path="assets/company.json",
)

users_with_companies = processor.associate_users_with_companies()

# You can save the filtered data to a JSON file using the save_data_to_json function. 
# In this example, we save the filtered user data to the "output_data.json" file.

output_json_file_path = "output_data.json"
processor.save_data_to_json(output_json_file_path, users_with_companies)
```


```
