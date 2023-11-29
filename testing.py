import os
import json

def parse_json_files_in_folder(folder_name):
    dataset_path = "dataset"
    if not os.path.exists(dataset_path):
        print(f"The dataset folder '{dataset_path}' does not exist.")
        return
    target_folder_path = os.path.join(dataset_path, folder_name)
    if not os.path.exists(target_folder_path) or not os.path.isdir(target_folder_path):
        print(f"The folder '{folder_name}' does not exist inside '{dataset_path}'.")
        return

    for root, dirs, files in os.walk(target_folder_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        return data
                except Exception as e:
                    print(f"Error parsing JSON file '{file_path}': {e}")
        

target_folder_name = "10.1145.3239261"
data = parse_json_files_in_folder(target_folder_name)
print(data)
