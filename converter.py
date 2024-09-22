import json

# Read the content from the 'data.txt' file
with open('data.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Parse the file content into a Python structure (list)
data = json.loads(file_content)

# Prepare the output in CSV format
output_lines = []

def process_coordinate_data(category, coordinates):
    """Processes coordinate data and appends it to the output."""
    for coord_pair in coordinates:
        if isinstance(coord_pair[0], list) and isinstance(coord_pair[1], list):
            lat1, lon1 = coord_pair[0]
            lat2, lon2 = coord_pair[1]
        elif isinstance(coord_pair[0], float) and isinstance(coord_pair[1], float):
            lat1, lon1 = coord_pair[0], coord_pair[1]
            lat2, lon2 = None, None  # Use None for second pair if not available
        else:
            continue  # Skip if the structure doesn't match expectations

        if lat2 is not None and lon2 is not None:
            output_lines.append(f"{category},{lat1},{lon1},{lat2},{lon2}")
        else:
            output_lines.append(f"{category},{lat1},{lon1},,")


def process_m_data(category, data_list, extra_value):
    """Processes 'm' type data and appends it to the output."""
    part1, part2, part3 = data_list
    output_lines.append(f"{category},{part1},{part2},{part3},{extra_value}")


# Parse through the data structure and process it
for item in data[1]:  # Assuming the relevant data is inside the second list
    if isinstance(item, list) and isinstance(item[0], str):
        # Handle string categories like "obliques", "traffic", "report_map_issue", etc.
        category = item[0]
        coordinates = item[1]
        process_coordinate_data(category, coordinates)
    elif isinstance(item, list) and isinstance(item[0], int):
        # Handle numeric categories like 20
        category = item[0]
        coordinates = item[1]
        process_coordinate_data(category, coordinates)
    elif isinstance(item, list) and len(item) == 3 and item[0] == "m":
        # Handle "m" data (e.g. ["m", [14, 14547, 6429], 706456825])
        category = item[0]
        data_list = item[1]
        extra_value = item[2]
        process_m_data(category, data_list, extra_value)

# Save the output to a CSV file
output_filename = 'output.csv'
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write("Category,Latitude1,Longitude1,Latitude2,Longitude2\n")  # Write header for coordinate data
    file.write("\n".join(output_lines))  # Write data

print(f"Data has been written to {output_filename}")
