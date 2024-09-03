import json
import csv

def flatten_json(json_object, parent_key='', separator='.'):
    items = {}
    for k, v in json_object.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, separator=separator))
        elif isinstance(v, list):
            items[new_key] = ';'.join(map(str, v))
        else:
            items[new_key] = v
    return items

if __name__ == "__main__":
    # Your JSON data. Normally you'd probably load this from a file or API.
    json_data = json.load(open('../data/sensor_data.json'))

    # Flatten the JSON data
    flat_data = [flatten_json(item) for item in json_data]

    # Write to CSV
    csv_file = '../data/flattened_data.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
        writer.writeheader()
        for row in flat_data:
            writer.writerow(row)

    print(f"Data written to {csv_file}")
