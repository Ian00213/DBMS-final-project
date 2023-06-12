import json

# Example input string
input_str = '{"friends": "NSCy54eWehBJyZdG2iE84w, pe42u7DcCH2QmI81NX-8qA, EjlCGf14tYMPJ0rsrL703w"}'

# Load the JSON string
data = json.loads(input_str)
print(data)
# Split the comma-separated string into a list
friends_list = data["friends"].split(", ")

# Update the data dictionary with the transformed list
data["friends"] = friends_list

# Print the updated data
print(data)