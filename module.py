from neo4j import GraphDatabase
import json
import time
import yaml

class neo4j:
    def __init__(self, user_name, password, database):
        self.user_name = user_name
        self.password = password
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user_name, password), database=database)
        self.session = self.driver.session()

    def flatten_properties(self, data, prefix=''):
        flattened_props = {}
        for key, value in data.items():
            if isinstance(value, dict):
                flattened_props.update(self.flatten_properties(value, prefix=f"{prefix}{key}_"))
            else:
                flattened_props[f"{prefix}{key}"] = value
        return flattened_props

    def create_node(self, node_name, data):
        flattened_properties = neo4j.flatten_properties(data)
        properties = ', '.join(f'{key}: {json.dumps(value)}' for key, value in flattened_properties.items())
        create_query = f'CREATE (n:{node_name} {{{properties}}});'
        self.session.run(create_query)

    def create_relationship(self, node1, node2, relationship):
        create_query = f'Match (n1:{node1}), (n2:{node2}) Create (n1)-[:{relationship}]->(n2);'
        self.session.run(create_query)

    def clear_all(self):
        clear_relationship_query = f'Match ()-[r]-() Delete r;'
        self.session.run(clear_relationship_query)
        clear_node_query = f'Match (n) DELETE n;'
        self.session.run(clear_node_query)

    def count_all(self):
        cnt_query = f'Match (n) Return count(n);'
        cnt_result = self.session.run(cnt_query)
        return cnt_result.single()[0]

    def close(self):
        self.session.close()



if __name__ == '__main__':
    user_name = "Ian"
    password = "Ian173859"
    database = "yelp"
    neo4j = neo4j(user_name, password, database)
    neo4j.clear_all()
    # 加载YAML文件
    with open('DBMS/dbfile.yml', 'r') as file:
        yaml_data = yaml.safe_load(file)
    yelp_files = yaml_data['yelp']
    for label, file_path in zip(list(yelp_files.keys()), list(yelp_files.values())):
    # raw_data_folder_path = "raw_data"
    # file_name = f"yelp_academic_dataset_business.json"
        with open(file_path, 'r', encoding="utf-8") as file:
            print(f"create nodes from {file.name}")
            start_time = time.time()
            for line_number, line in enumerate(file):
                if line_number >= 10000:
                    break
                data = json.loads(line)
                if label == "User":
                    friends_list = data["friends"].split(", ")
                    data["friends"] = friends_list
                neo4j.create_node(label, data)
            end_time = time.time()
            print(f"{file.name} time taken: {end_time - start_time} seconds")
            # neo4j.close()