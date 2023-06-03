from neo4j import GraphDatabase
import pandas as pd

user_name = input("Enter the user name: ")
password = input("Enter the password: ")

# Connect to the database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user_name, password))

# Create a session to run Cypher statements in
session = driver.session()

# user input
user_input = input("Enter a name or a relationship type: ")

# Write a Cypher statement
query = "MATCH (n1)-[r]->(n2) RETURN (n1), (r), (n2)"

# Run a Cypher statement
result = session.run(query)
result
data = []
# Extract the data from the result
for record in result:
    data.append(record)
data
# Extract first record that matches the query
print(data[0])


# Create a DataFrame from the data
df = pd.DataFrame([], columns=["n1", "r", "n2"])

for i in range(0, len(data)):
    if user_input in str(data[i]["r"].type) or user_input in str(data[i]["n1"]._properties):
        print(data[i]["n1"]["name"], data[i]["r"].type, data[i]["n2"]["name"])
        df = df.append({"n1": data[i]["n1"]["name"], "r": data[i]["r"].type, "n2": data[i]["n2"]["name"]}, ignore_index=True)
    else:
        pass
print(df)

# # Print the DataFrame
# print(df)