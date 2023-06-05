import json
import os

raw_data_folder_path = "raw_data"
transformed_data_folder_path = "transformed_data"

json_data = []

table_list = ["business", "checkin", "review", "tip", "user"]
for table in table_list:

    file_name = f"yelp_academic_dataset_{table}.json"

    if not os.path.exists(f"{transformed_data_folder_path}/transformed_{file_name}"):
        with open(f"{raw_data_folder_path}/{file_name}", 'r', encoding="utf-8") as file:
            for line_number, line in enumerate(file):
                if line_number >= 10000:
                    break
                obj = json.loads(line)
                json_data.append(obj)

        output_data = {"data": json_data}

        with open(f"{transformed_data_folder_path}/transformed_{file_name}", 'w', encoding="utf-8") as output_file:
            json.dump(output_data, output_file)

        print(f"Data transformation complete. The transformed data is saved in transformed_{file_name}.")
    else:
        print("The transformed data folder already exists. Skipping data transformation.")

