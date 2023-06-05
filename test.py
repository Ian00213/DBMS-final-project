from neo4j import GraphDatabase
import json
import time

user_name = input("Enter the user name: ")
password = input("Enter the password: ")

# Connect to the database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user_name, password))

# Create a session to run Cypher statements in
session = driver.session()

raw_data_folder_path = "raw_data"
file_name = f"yelp_academic_dataset_business.json"

def flatten_properties(properties, prefix=''):
    flattened_props = {}
    for key, value in properties.items():
        if isinstance(value, dict):
            flattened_props.update(flatten_properties(value, prefix=f"{prefix}{key}_"))
        else:
            flattened_props[f"{prefix}{key}"] = value
    return flattened_props



with open(f"{raw_data_folder_path}/{file_name}", 'r', encoding="utf-8") as file:
    clear_query = f'Match (n) DELETE n;'
    session.run(clear_query)

    # start timer
    start_time = time.time()
    for line_number, line in enumerate(file):
        if line_number >= 10000:
            break
        data = json.loads(line)
        flattened_properties = flatten_properties(data)
        properties = ', '.join(f'{key}: {json.dumps(value)}' for key, value in flattened_properties.items())
        create_query = f'CREATE (b:business {{{properties}}});'
        session.run(create_query)

    # end timer
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

cnt_query = f'Match (n) Return count(n);'
cnt_result = session.run(cnt_query)
cnt_result
print(f"total_nodes: {cnt_result.single()[0]}")