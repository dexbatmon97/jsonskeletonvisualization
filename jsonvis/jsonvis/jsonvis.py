import json

def load_json(file_path):
    """ Load JSON data from a file """
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json(data1, data2, path=""):
    """ Recursively compare two JSON objects """
    if type(data1) != type(data2):
        print(f"Type mismatch at {path}: {type(data1)} vs {type(data2)}")
        return

    if isinstance(data1, dict):
        for key in data1.keys():
            if key not in data2:
                print(f"Missing {path}.{key} in second JSON")
            else:
                compare_json(data1[key], data2[key], path + "." + key)
        for key in data2.keys():
            if key not in data1:
                print(f"Missing {path}.{key} in first JSON")
    elif isinstance(data1, list):
        if len(data1) != len(data2):
            print(f"List length mismatch at {path}: {len(data1)} vs {len(data2)}")
        else:
            for i in range(len(data1)):
                compare_json(data1[i], data2[i], path + f"[{i}]")
    else:
        if data1 != data2:
            print(f"Value mismatch at {path}: {data1} vs {data2}")

# Load JSON files
file1 = "C:\\Users\\evillaro\\Downloads\\outputtest.json"
file2 = "C:\\Users\\evillaro\\Downloads\\output.json"

data1 = load_json(file1)
data2 = load_json(file2)

# Compare JSON files
print("Comparing JSON files...")
compare_json(data1, data2)