import sqlite3  # Library to handle SQLite database connections
import snappy  # Library to handle data compression/decompression
import json  # Library for handling JSON data
import re  # Library for Regular Expressions

# Connect to the SQLite database
# Replace "3647222921wleabcEoxlt-eengsairo.sqlite" with your actual database file
database_path = "3647222921wleabcEoxlt-eengsairo.sqlite"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Initialize an empty list to store decompressed data
decompressed_data = []

# Query all rows from the `object_data` table
data = cursor.execute("SELECT * FROM object_data;").fetchall()
aux= len(data)
print("length of data:" , aux)

# Loop through the first 45 rows of the result set
for row_index in range(aux):  # Adjust range as needed for your dataset
    # Decompress the data from the 5th column (index 4) of each row
    decompressed_data.append(snappy.decompress(data[row_index][4]))

# Convert the decompressed data list to a single string
decompressed_data_str = str(decompressed_data)
print(decompressed_data_str)

# Extract and print specific segments of the data for analysis
# Extract a section around the keyword "iterations"
iterations_segment = decompressed_data_str[
    decompressed_data_str.find('iterations') - 1: decompressed_data_str.find('iterations') + 18
]
print(iterations_segment)

# Extract a section around the keyword "email"
email_segment = decompressed_data_str[
    decompressed_data_str.find('email') - 1: decompressed_data_str.find('email') + 22
]
print(email_segment)

# Extract a section around the keyword "kdfType"
kdf_type_segment = decompressed_data_str[
    decompressed_data_str.find('kdfType') - 1: decompressed_data_str.find('kdfType') + 10
]
print(kdf_type_segment)

pattern = r'"(.{44})"' #the key is composed of 44 characters and its encclosed in double quotes so to find it we can use this pattern to out advantage
matches = re.findall(pattern, decompressed_data_str)

# Print the results
print("44-character words enclosed in double quotes (possible master key hash):")
for match in matches:
    print(match)

# Optional: Save the decompressed data to a text file (uncomment if needed)
# with open("output.txt", "a") as output_file:
#     output_file.write(str(decompressed_data))

# Close the database connection
connection.close()
